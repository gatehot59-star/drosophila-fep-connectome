#!/usr/bin/env python3
"""Tests for the ROI-compartment and population manifest contract."""
from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from h4_roi_compartment_manifest import RoiCompartmentError, build_manifest  # noqa: E402

ANNOTATION_HEADER = ["root_id", "super_class", "cell_class", "flow", "supertype", "cell_type", "top_nt", "top_nt_conf", "side"]
MAPPING_HEADER = ["animal_id", "trial_id", "roi_name", "roi_unit", "mapping_status", "region_label", "root_ids", "root_weights", "evidence_kind", "confidence", "notes"]


def write_table(path: Path, header: list[str], rows: list[list[str]]) -> None:
    """Write a deterministic TSV fixture."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def fixture(directory: str, rows: list[list[str]]) -> tuple[Path, Path]:
    """Create annotation and mapping fixtures."""
    root = Path(directory)
    annotations = root / "annotations.tsv"
    mapping = root / "mapping.tsv"
    write_table(annotations, ANNOTATION_HEADER, [["101", "central", "a", "in", "a", "cell_a", "acetylcholine", "0.9", "left"], ["202", "visual", "b", "out", "b", "cell_b", "glutamate", "0.8", "right"]])
    write_table(mapping, MAPPING_HEADER, rows)
    return mapping, annotations


class RoiCompartmentManifestTests(unittest.TestCase):
    """Exercise unmapped, regional and population contracts."""

    def test_unmapped_compartments_are_explicit_and_safe(self):
        """Public R65D11-style rows produce descriptive UNMAPPED output."""
        with tempfile.TemporaryDirectory() as directory:
            rows = [["fly1", "1", "ROI_0", "ROI_COMPARTMENT", "UNMAPPED", "", "", "", "unmapped", "0", "no geometry"], ["fly1", "1", "ROI_1", "POPULATION", "UNMAPPED", "", "", "", "unmapped", "0", "no geometry"]]
            mapping, annotations = fixture(directory, rows)
            result = build_manifest(mapping, annotations, [("1", "ROI_0"), ("1", "ROI_1")])
            self.assertEqual(result["mapping_verdict"], "UNMAPPED")
            self.assertEqual(result["counts"]["unmapped_rows"], 2)

    def test_region_mapping_requires_region_evidence(self):
        """A regional claim must name its region and evidence kind."""
        with tempfile.TemporaryDirectory() as directory:
            rows = [["fly1", "1", "ROI_0", "REGION", "REGION_MAPPED", "cervical_connective", "", "", "manual_region", "0.8", "operator note"], ["fly1", "1", "ROI_1", "REGION", "REGION_MAPPED", "cervical_connective", "", "", "manual_region", "0.8", "operator note"]]
            mapping, annotations = fixture(directory, rows)
            result = build_manifest(mapping, annotations, [("1", "ROI_0"), ("1", "ROI_1")])
            self.assertEqual(result["mapping_verdict"], "REGIONAL")
            self.assertEqual(result["counts"]["region_rows"], 2)

    def test_population_mapping_requires_weights_that_sum_to_one(self):
        """Population root IDs must have aligned normalized weights."""
        with tempfile.TemporaryDirectory() as directory:
            rows = [["fly1", "1", "ROI_0", "POPULATION", "POPULATION_MAPPED", "", "101;202", "0.25;0.75", "manual_population", "0.7", "operator note"], ["fly1", "1", "ROI_1", "POPULATION", "UNMAPPED", "", "", "", "unmapped", "0", "no geometry"]]
            mapping, annotations = fixture(directory, rows)
            result = build_manifest(mapping, annotations, [("1", "ROI_0"), ("1", "ROI_1")])
            self.assertEqual(result["mapping_verdict"], "POPULATION_MAPPED")
            self.assertEqual(result["rows"][0]["root_ids"], [101, 202])

    def test_rejects_population_weights_that_do_not_sum_to_one(self):
        """Invalid mixture weights cannot pass the contract."""
        with tempfile.TemporaryDirectory() as directory:
            rows = [["fly1", "1", "ROI_0", "POPULATION", "POPULATION_MAPPED", "", "101;202", "0.2;0.2", "manual_population", "0.7", "bad weights"], ["fly1", "1", "ROI_1", "POPULATION", "UNMAPPED", "", "", "", "unmapped", "0", "no geometry"]]
            mapping, annotations = fixture(directory, rows)
            with self.assertRaisesRegex(RoiCompartmentError, "sum to 1"):
                build_manifest(mapping, annotations, [("1", "ROI_0"), ("1", "ROI_1")])

    def test_rejects_root_id_absent_from_annotations(self):
        """A population cannot smuggle an unknown root ID into the manifest."""
        with tempfile.TemporaryDirectory() as directory:
            rows = [["fly1", "1", "ROI_0", "POPULATION", "POPULATION_MAPPED", "", "999;202", "0.5;0.5", "manual_population", "0.7", "unknown root"], ["fly1", "1", "ROI_1", "POPULATION", "UNMAPPED", "", "", "", "unmapped", "0", "no geometry"]]
            mapping, annotations = fixture(directory, rows)
            with self.assertRaisesRegex(RoiCompartmentError, "absent from annotation"):
                build_manifest(mapping, annotations, [("1", "ROI_0"), ("1", "ROI_1")])

    def test_rejects_missing_trial_roi_pair(self):
        """Every expected trial and ROI pair must be present exactly once."""
        with tempfile.TemporaryDirectory() as directory:
            rows = [["fly1", "1", "ROI_0", "ROI_COMPARTMENT", "UNMAPPED", "", "", "", "unmapped", "0", "no geometry"]]
            mapping, annotations = fixture(directory, rows)
            with self.assertRaisesRegex(RoiCompartmentError, "trial/ROI set differs"):
                build_manifest(mapping, annotations, [("1", "ROI_0"), ("1", "ROI_1")])


if __name__ == "__main__":
    unittest.main()
