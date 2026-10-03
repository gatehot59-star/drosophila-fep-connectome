#!/usr/bin/env python3
"""Contracts for the explicit ROI-to-FlyWire mapping gate."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from h4_roi_anatomy_manifest import RoiAnatomyError, build_manifest  # noqa: E402


ANNOTATION_HEADER = ["root_id", "super_class", "cell_class", "flow", "supertype", "cell_type", "top_nt", "top_nt_conf", "side"]
MAPPING_HEADER = ["roi_name", "root_id", "mapping_status", "evidence_kind", "confidence", "notes"]


def write_table(path: Path, header: list[str], rows: list[list[str]]) -> None:
    """Write a deterministic TSV fixture."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def fixture(directory: str, mapping_rows: list[list[str]], annotation_rows: list[list[str]] | None = None) -> tuple[Path, Path]:
    """Create a mapping and annotation fixture."""
    root = Path(directory)
    annotations = root / "annotations.tsv"
    mapping = root / "mapping.tsv"
    write_table(annotations, ANNOTATION_HEADER, annotation_rows or [
        ["101", "central", "class_a", "in", "type_a", "cell_a", "acetylcholine", "0.9", "left"],
        ["202", "visual_projection", "class_b", "out", "type_b", "cell_b", "glutamate", "0.8", "right"],
    ])
    write_table(mapping, MAPPING_HEADER, mapping_rows)
    return mapping, annotations


class RoiAnatomyManifestTests(unittest.TestCase):
    """Exercise positive, partial and fail-closed mapping contracts."""

    def test_complete_mapping_joins_only_declared_root_ids(self):
        """A complete explicit map receives the pinned annotation payload."""
        with tempfile.TemporaryDirectory() as directory:
            mapping, annotations = fixture(directory, [["ROI_0", "101", "MAPPED", "direct_root_id", "1.0", "segmentation manifest"], ["ROI_1", "202", "MAPPED", "manual_roi_to_cell", "0.8", "manual cell identity"]])
            result = build_manifest(mapping, annotations, ["ROI_0", "ROI_1"])
            self.assertEqual(result["verdict"], "BIEN")
            self.assertEqual(result["mapping_verdict"], "COMPLETE")
            self.assertEqual(result["counts"]["mapped_rois"], 2)
            self.assertEqual(result["rois"][0]["annotation"]["cell_type"], "cell_a")

    def test_partial_mapping_is_explicit_not_inferred(self):
        """An unmapped ROI is accepted only as an explicit unmapped row."""
        with tempfile.TemporaryDirectory() as directory:
            mapping, annotations = fixture(directory, [["ROI_0", "101", "MAPPED", "direct_root_id", "1.0", "segmentation manifest"], ["ROI_1", "", "UNMAPPED", "unmapped", "0", "no source identity"]])
            result = build_manifest(mapping, annotations, ["ROI_0", "ROI_1"])
            self.assertEqual(result["mapping_verdict"], "PARTIAL")
            self.assertIsNone(result["rois"][1]["root_id"])

    def test_rejects_unknown_root_id(self):
        """A root ID absent from the annotation snapshot cannot pass."""
        with tempfile.TemporaryDirectory() as directory:
            mapping, annotations = fixture(directory, [["ROI_0", "999", "MAPPED", "direct_root_id", "1.0", "unknown"], ["ROI_1", "202", "MAPPED", "direct_root_id", "1.0", "known"]])
            with self.assertRaisesRegex(RoiAnatomyError, "absent from annotation"):
                build_manifest(mapping, annotations, ["ROI_0", "ROI_1"])

    def test_rejects_missing_roi_name(self):
        """The expected ROI set must be complete."""
        with tempfile.TemporaryDirectory() as directory:
            mapping, annotations = fixture(directory, [["ROI_0", "101", "MAPPED", "direct_root_id", "1.0", "known"]])
            with self.assertRaisesRegex(RoiAnatomyError, "ROI set differs"):
                build_manifest(mapping, annotations, ["ROI_0", "ROI_1"])

    def test_rejects_duplicate_root_id(self):
        """Two ROI channels cannot silently alias one FlyWire cell."""
        with tempfile.TemporaryDirectory() as directory:
            mapping, annotations = fixture(directory, [["ROI_0", "101", "MAPPED", "direct_root_id", "1.0", "first"], ["ROI_1", "101", "MAPPED", "direct_root_id", "1.0", "duplicate"]])
            with self.assertRaisesRegex(RoiAnatomyError, "assigned to more than one"):
                build_manifest(mapping, annotations, ["ROI_0", "ROI_1"])

    def test_rejects_region_only_claim_as_cell_mapping(self):
        """A region label cannot masquerade as a root-ID mapping."""
        with tempfile.TemporaryDirectory() as directory:
            mapping, annotations = fixture(directory, [["ROI_0", "101", "MAPPED", "region_only", "1.0", "region only"], ["ROI_1", "202", "MAPPED", "direct_root_id", "1.0", "known"]])
            with self.assertRaisesRegex(RoiAnatomyError, "direct or manual cell"):
                build_manifest(mapping, annotations, ["ROI_0", "ROI_1"])

    def test_rejects_duplicate_annotation_root_id(self):
        """The annotation snapshot itself must be unique by root ID."""
        with tempfile.TemporaryDirectory() as directory:
            duplicate_annotations = [["101", "central", "a", "in", "a", "a", "acetylcholine", "0.9", "left"], ["101", "central", "b", "in", "b", "b", "acetylcholine", "0.9", "left"]]
            mapping, annotations = fixture(directory, [["ROI_0", "101", "MAPPED", "direct_root_id", "1.0", "known"], ["ROI_1", "202", "MAPPED", "direct_root_id", "1.0", "known"]], duplicate_annotations)
            with self.assertRaisesRegex(RoiAnatomyError, "duplicate root_id"):
                build_manifest(mapping, annotations, ["ROI_0", "ROI_1"])


if __name__ == "__main__":
    unittest.main()
