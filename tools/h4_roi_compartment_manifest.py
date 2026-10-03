#!/usr/bin/env python3
"""Validate ROI-compartment or population provenance without cell inference."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Sequence

SCHEMA = "h4-roi-compartment-map/v1"
MAPPING_COLUMNS = (
    "animal_id",
    "trial_id",
    "roi_name",
    "roi_unit",
    "mapping_status",
    "region_label",
    "root_ids",
    "root_weights",
    "evidence_kind",
    "confidence",
    "notes",
)
ANNOTATION_COLUMNS = ("root_id", "super_class", "cell_class", "flow", "supertype", "cell_type", "top_nt", "top_nt_conf", "side")
UNMAPPED_UNITS = frozenset({"ROI_COMPARTMENT", "POPULATION", "UNKNOWN"})


class RoiCompartmentError(ValueError):
    """Raised when a compartment manifest violates its explicit contract."""


def md5_file(path: Path) -> str:
    """Return the MD5 digest of a provenance input."""
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _required_columns(fieldnames: Sequence[str] | None, required: Sequence[str], name: str) -> None:
    """Require all columns in a tabular contract."""
    if fieldnames is None:
        raise RoiCompartmentError(f"{name}: missing header")
    missing = sorted(set(required) - set(fieldnames))
    if missing:
        raise RoiCompartmentError(f"{name}: missing columns {missing}")


def _positive_int(value: str, field: str) -> int:
    """Parse a strictly positive integer."""
    try:
        parsed = int(value.strip())
    except ValueError as exc:
        raise RoiCompartmentError(f"{field}: expected positive integer") from exc
    if parsed <= 0:
        raise RoiCompartmentError(f"{field}: expected positive integer")
    return parsed


def _confidence(value: str, field: str) -> float:
    """Parse finite confidence in the closed interval [0, 1]."""
    try:
        parsed = float(value.strip())
    except ValueError as exc:
        raise RoiCompartmentError(f"{field}: expected numeric confidence") from exc
    if not math.isfinite(parsed) or not 0.0 <= parsed <= 1.0:
        raise RoiCompartmentError(f"{field}: confidence must be finite and between 0 and 1")
    return parsed


def load_annotations(path: Path) -> dict[int, dict[str, str]]:
    """Load the pinned annotation snapshot indexed by root ID."""
    if not path.is_file():
        raise RoiCompartmentError(f"annotations file does not exist: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        _required_columns(reader.fieldnames, ANNOTATION_COLUMNS, "annotations")
        result: dict[int, dict[str, str]] = {}
        for line_number, row in enumerate(reader, start=2):
            root = _positive_int((row.get("root_id") or ""), f"annotations line {line_number}")
            if root in result:
                raise RoiCompartmentError(f"annotations line {line_number}: duplicate root_id {root}")
            result[root] = {column: (row.get(column) or "").strip() for column in ANNOTATION_COLUMNS if column != "root_id"}
    if not result:
        raise RoiCompartmentError("annotations: no rows")
    return result


def _parse_semicolon_floats(value: str, field: str) -> list[float]:
    """Parse a non-empty semicolon-separated list of finite floats."""
    try:
        values = [float(token.strip()) for token in value.split(";") if token.strip()]
    except ValueError as exc:
        raise RoiCompartmentError(f"{field}: invalid semicolon-separated float list") from exc
    if not values or not all(math.isfinite(item) and item > 0 for item in values):
        raise RoiCompartmentError(f"{field}: values must be finite and positive")
    return values


def _parse_semicolon_roots(value: str, field: str) -> list[int]:
    """Parse a non-empty semicolon-separated list of positive root IDs."""
    values = [_positive_int(token, field) for token in value.split(";") if token.strip()]
    if not values or len(set(values)) != len(values):
        raise RoiCompartmentError(f"{field}: root IDs must be non-empty and unique")
    return values


def load_mapping(path: Path, expected_pairs: Sequence[tuple[str, str]], annotations: dict[int, dict[str, str]]) -> list[dict[str, Any]]:
    """Load and validate one row for every expected trial and ROI pair."""
    if not path.is_file():
        raise RoiCompartmentError(f"mapping file does not exist: {path}")
    expected = tuple(expected_pairs)
    if not expected or len(set(expected)) != len(expected):
        raise RoiCompartmentError("expected trial/ROI pairs must be non-empty and unique")
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        _required_columns(reader.fieldnames, MAPPING_COLUMNS, "mapping")
        for line_number, row in enumerate(reader, start=2):
            animal_id = (row.get("animal_id") or "").strip()
            trial_id = (row.get("trial_id") or "").strip()
            roi_name = (row.get("roi_name") or "").strip()
            if not animal_id or not trial_id or not roi_name:
                raise RoiCompartmentError(f"mapping line {line_number}: animal_id, trial_id and roi_name are required")
            pair = (trial_id, roi_name)
            if pair in seen:
                raise RoiCompartmentError(f"mapping line {line_number}: duplicate trial/ROI pair {pair}")
            seen.add(pair)
            unit = (row.get("roi_unit") or "").strip().upper()
            status = (row.get("mapping_status") or "").strip().upper()
            region = (row.get("region_label") or "").strip()
            root_text = (row.get("root_ids") or "").strip()
            weight_text = (row.get("root_weights") or "").strip()
            evidence = (row.get("evidence_kind") or "").strip()
            notes = (row.get("notes") or "").strip()
            confidence = _confidence((row.get("confidence") or ""), f"mapping line {line_number}")
            if unit not in {"ROI_COMPARTMENT", "POPULATION", "REGION", "UNKNOWN"}:
                raise RoiCompartmentError(f"mapping line {line_number}: unsupported roi_unit {unit}")
            if status not in {"UNMAPPED", "REGION_MAPPED", "POPULATION_MAPPED"}:
                raise RoiCompartmentError(f"mapping line {line_number}: unsupported mapping_status {status}")
            parsed_roots: list[int] = []
            parsed_weights: list[float] = []
            if status == "UNMAPPED":
                if unit not in UNMAPPED_UNITS or region or root_text or weight_text or evidence != "unmapped" or confidence != 0.0:
                    raise RoiCompartmentError(f"mapping line {line_number}: UNMAPPED row contains mapping evidence")
            elif status == "REGION_MAPPED":
                if unit != "REGION" or not region or root_text or weight_text or evidence not in {"direct_region", "manual_region"} or not notes:
                    raise RoiCompartmentError(f"mapping line {line_number}: invalid REGION_MAPPED contract")
            else:
                if unit not in {"POPULATION", "ROI_COMPARTMENT"} or region or not root_text or not weight_text or evidence not in {"direct_population", "manual_population"} or not notes:
                    raise RoiCompartmentError(f"mapping line {line_number}: invalid POPULATION_MAPPED contract")
                parsed_roots = _parse_semicolon_roots(root_text, f"mapping line {line_number} root_ids")
                parsed_weights = _parse_semicolon_floats(weight_text, f"mapping line {line_number} root_weights")
                if len(parsed_roots) != len(parsed_weights) or not math.isclose(sum(parsed_weights), 1.0, rel_tol=0.0, abs_tol=1e-6):
                    raise RoiCompartmentError(f"mapping line {line_number}: root_ids and root_weights must align and sum to 1")
                missing = [root for root in parsed_roots if root not in annotations]
                if missing:
                    raise RoiCompartmentError(f"mapping line {line_number}: root IDs absent from annotation snapshot {missing}")
            rows.append({"animal_id": animal_id, "trial_id": trial_id, "roi_name": roi_name, "roi_unit": unit, "mapping_status": status, "region_label": region, "root_ids": parsed_roots, "root_weights": parsed_weights, "evidence_kind": evidence, "confidence": confidence, "notes": notes})
    if set(expected) != seen:
        raise RoiCompartmentError(f"mapping trial/ROI set differs: expected {sorted(expected)}, got {sorted(seen)}")
    return [next(row for row in rows if (row["trial_id"], row["roi_name"]) == pair) for pair in expected]


def build_manifest(mapping_path: Path, annotations_path: Path, expected_pairs: Sequence[tuple[str, str]]) -> dict[str, Any]:
    """Build a population-safe manifest without assigning cellular identity."""
    annotations = load_annotations(annotations_path)
    rows = load_mapping(mapping_path, expected_pairs, annotations)
    statuses = {row["mapping_status"] for row in rows}
    verdict = "UNMAPPED" if statuses == {"UNMAPPED"} else ("REGIONAL" if "POPULATION_MAPPED" not in statuses else "POPULATION_MAPPED")
    return {"schema": SCHEMA, "verdict": "BIEN", "mapping_verdict": verdict, "expected_pairs": [{"trial_id": trial, "roi_name": roi} for trial, roi in expected_pairs], "counts": {"row_count": len(rows), "unmapped_rows": sum(row["mapping_status"] == "UNMAPPED" for row in rows), "region_rows": sum(row["mapping_status"] == "REGION_MAPPED" for row in rows), "population_rows": sum(row["mapping_status"] == "POPULATION_MAPPED" for row in rows), "annotation_rows": len(annotations)}, "inputs": {"mapping": {"path": str(mapping_path), "bytes": mapping_path.stat().st_size, "md5": md5_file(mapping_path)}, "annotations": {"path": str(annotations_path), "bytes": annotations_path.stat().st_size, "md5": md5_file(annotations_path)}}, "rows": rows, "limitations": ["This manifest describes compartments, regions or populations; it never claims a single ROI is a neuron.", "UNMAPPED rows support descriptive analysis only.", "A REGION_MAPPED or POPULATION_MAPPED row does not establish causal route identity."]}


def main(argv: Sequence[str] | None = None) -> int:
    """Validate a mapping TSV from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--trial", dest="trials", action="append", required=True)
    parser.add_argument("--roi", dest="rois", action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        pairs = [(trial, roi) for trial in args.trials for roi in args.rois]
        manifest = build_manifest(args.mapping, args.annotations, pairs)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"verdict": manifest["verdict"], "mapping_verdict": manifest["mapping_verdict"], "counts": manifest["counts"], "out": str(args.out)}, sort_keys=True))
        return 0
    except (OSError, csv.Error, RoiCompartmentError, ValueError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
