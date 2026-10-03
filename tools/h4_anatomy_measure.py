#!/usr/bin/env python3
"""Measure confocal stack geometry and labeled-volume occupancy without ROI mapping."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import tifffile


class AnatomyMeasureError(ValueError):
    """Raised when a confocal stack cannot support the declared measurement."""


def md5_file(path: Path) -> str:
    """Return the MD5 digest of a local stack."""
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def otsu_threshold(histogram: np.ndarray) -> int:
    """Return an 8-bit Otsu threshold from a complete image histogram."""
    counts = np.asarray(histogram, dtype=np.float64)
    if counts.shape != (256,) or counts.sum() <= 0:
        raise AnatomyMeasureError("histogram must contain 256 non-empty bins")
    levels = np.arange(256, dtype=np.float64)
    total = counts.sum()
    total_mean = float((levels * counts).sum() / total)
    weight = 0.0
    mean = 0.0
    best = -1.0
    threshold = 0
    for level in range(256):
        weight += counts[level]
        mean += level * counts[level]
        if weight <= 0.0 or weight >= total:
            continue
        between = ((total_mean * weight - mean) ** 2) / (weight * (total - weight))
        if between > best:
            best = between
            threshold = level
    return threshold


def _voxel_size_um(lsm_info: dict[str, Any]) -> tuple[float, float, float]:
    """Read LSM voxel sizes and convert meters to micrometers."""
    values = tuple(float(lsm_info[key]) * 1e6 for key in ("VoxelSizeX", "VoxelSizeY", "VoxelSizeZ"))
    if not all(math.isfinite(value) and value > 0 for value in values):
        raise AnatomyMeasureError("LSM voxel sizes must be finite and positive")
    return values


def _series_geometry(tf: tifffile.TiffFile) -> tuple[tifffile.TiffPageSeries, dict[str, Any]]:
    """Select the full-resolution ZCYX series and its LSM metadata."""
    if not tf.series:
        raise AnatomyMeasureError("stack has no TIFF series")
    series = next((item for item in tf.series if item.axes == "ZCYX"), tf.series[0])
    if series.axes != "ZCYX" or len(series.shape) != 4:
        raise AnatomyMeasureError(f"expected full-resolution ZCYX series, got {series.axes} {series.shape}")
    page = tf.pages[0]
    tag = page.tags.get(34412)
    if tag is None or not isinstance(tag.value, dict):
        raise AnatomyMeasureError("stack has no readable CZ_LSMINFO metadata")
    return series, tag.value


def measure_stack(path: Path) -> dict[str, Any]:
    """Measure physical geometry and thresholded foreground per fluorescence channel."""
    if not path.is_file():
        raise AnatomyMeasureError(f"stack does not exist: {path}")
    with tifffile.TiffFile(path) as tf:
        series, lsm_info = _series_geometry(tf)
        z_count, channel_count, height, width = (int(value) for value in series.shape)
        voxel_x, voxel_y, voxel_z = _voxel_size_um(lsm_info)
        histograms = np.zeros((channel_count, 256), dtype=np.int64)
        for z in range(z_count):
            image = tf.pages[2 * z].asarray()
            if image.shape != (channel_count, height, width):
                raise AnatomyMeasureError(f"unexpected page shape at z={z}: {image.shape}")
            for channel in range(channel_count):
                histograms[channel] += np.bincount(image[channel].ravel(), minlength=256)
        thresholds = [otsu_threshold(histograms[channel]) for channel in range(channel_count)]
        stats: list[dict[str, Any]] = []
        for channel, threshold in enumerate(thresholds):
            foreground = 0
            min_xyz = [width, height, z_count]
            max_xyz = [-1, -1, -1]
            plane_counts: list[int] = []
            for z in range(z_count):
                image = tf.pages[2 * z].asarray()[channel]
                mask = image > threshold
                ys, xs = np.nonzero(mask)
                count = int(mask.sum())
                plane_counts.append(count)
                foreground += count
                if count:
                    min_xyz = [min(min_xyz[0], int(xs.min())), min(min_xyz[1], int(ys.min())), min(min_xyz[2], z)]
                    max_xyz = [max(max_xyz[0], int(xs.max())), max(max_xyz[1], int(ys.max())), max(max_xyz[2], z)]
            volume_um3 = foreground * voxel_x * voxel_y * voxel_z
            bbox_voxels = [max_xyz[index] - min_xyz[index] + 1 for index in range(3)] if max_xyz[0] >= 0 else [0, 0, 0]
            stats.append({
                "channel": channel,
                "otsu_threshold": threshold,
                "foreground_voxels": foreground,
                "foreground_fraction": foreground / (z_count * height * width),
                "foreground_volume_um3": volume_um3,
                "bbox_voxels_xyz": bbox_voxels,
                "bbox_um_xyz": [bbox_voxels[0] * voxel_x, bbox_voxels[1] * voxel_y, bbox_voxels[2] * voxel_z],
                "bbox_min_xyz_voxels": min_xyz,
                "bbox_max_xyz_voxels": max_xyz,
                "peak_plane_z": int(np.argmax(plane_counts)) if plane_counts else None,
                "peak_plane_foreground_voxels": max(plane_counts) if plane_counts else 0,
            })
        return {
            "schema": "h4-confocal-anatomy-measure/v1",
            "verdict": "BIEN",
            "source": {
                "file": path.name,
                "bytes": path.stat().st_size,
                "md5": md5_file(path),
                "format": "Zeiss LSM/TIFF",
                "dataset": "doi:10.7910/DVN/KTQT27",
            },
            "acquisition": {
                "series_axes": series.axes,
                "shape_zcyx": [z_count, channel_count, height, width],
                "voxel_um_xyz": [voxel_x, voxel_y, voxel_z],
                "field_of_view_um_xyz": [width * voxel_x, height * voxel_y, z_count * voxel_z],
                "objective": lsm_info.get("ScanInformation", {}).get("Objective", ""),
                "scan_name": lsm_info.get("ScanInformation", {}).get("Name", ""),
            },
            "channels": stats,
            "interpretation": [
                "This is quantitative anatomy of the R65D11 confocal driver-line sample.",
                "Foreground is an intensity-thresholded labeled volume, not a cell identity assignment.",
                "The confocal sample is not the functional two-photon trial; no ROI_0 or ROI_1 mapping is inferred.",
            ],
        }


def main() -> int:
    """Measure one local LSM stack and write a JSON receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = measure_stack(args.stack)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"verdict": result["verdict"], "file": result["source"]["file"], "md5": result["source"]["md5"], "shape_zcyx": result["acquisition"]["shape_zcyx"], "out": str(args.out)}, sort_keys=True))
        return 0
    except (OSError, KeyError, TypeError, ValueError, tifffile.TiffFileError, AnatomyMeasureError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
