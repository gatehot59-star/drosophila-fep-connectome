#!/usr/bin/env python3
"""Stress-test the ROI regional-null boundary without inventing anatomy."""
from __future__ import annotations

import argparse
import csv
import json
import re
import tempfile
from pathlib import Path
from typing import Any, Callable

from h4_roi_compartment_manifest import RoiCompartmentError, build_manifest

EXPECTED_PAIRS = (("1", "ROI_0"), ("1", "ROI_1"))
ANNOTATION_HEADER = [
    "root_id",
    "super_class",
    "cell_class",
    "flow",
    "supertype",
    "cell_type",
    "top_nt",
    "top_nt_conf",
    "side",
]
MAPPING_HEADER = [
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
]


class RegionalNullStressError(ValueError):
    """Raised when a regional-null input violates the explicit boundary."""


def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    """Write a deterministic TSV fixture for one stress case."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def annotations_rows() -> list[list[str]]:
    """Return the minimal annotation snapshot used by synthetic cases."""
    return [
        ["101", "central", "a", "in", "a", "cell_a", "acetylcholine", "0.9", "left"],
        ["202", "visual", "b", "out", "b", "cell_b", "glutamate", "0.8", "right"],
    ]


def valid_region_rows() -> list[list[str]]:
    """Return two explicitly evidenced regional rows."""
    return [
        [
            "fly1",
            "1",
            "ROI_0",
            "REGION",
            "REGION_MAPPED",
            "central_complex",
            "",
            "",
            "manual_region",
            "0.8",
            "operator mapped ROI to central complex from source record",
        ],
        [
            "fly1",
            "1",
            "ROI_1",
            "REGION",
            "REGION_MAPPED",
            "central_complex",
            "",
            "",
            "manual_region",
            "0.8",
            "operator mapped ROI to central complex from source record",
        ],
    ]


def valid_unmapped_row(roi_name: str) -> list[str]:
    """Return one explicit unmapped row."""
    return [
        [
            "fly1",
            "1",
            roi_name,
            "ROI_COMPARTMENT",
            "UNMAPPED",
            "",
            "",
            "",
            "unmapped",
            "0",
            "no geometry",
        ]
    ][0]


def evaluate_regional_input(manifest: dict[str, Any]) -> None:
    """Reject every regional input without complete explicit region provenance."""
    if manifest.get("mapping_verdict") != "REGIONAL":
        raise RegionalNullStressError("regional null requires mapping_verdict=REGIONAL")
    rows = manifest.get("rows", [])
    if not rows:
        raise RegionalNullStressError("regional null requires explicit rows")
    if any(row.get("mapping_status") != "REGION_MAPPED" for row in rows):
        raise RegionalNullStressError("regional null rejects mixed or non-regional rows")
    for row in rows:
        label = str(row.get("region_label", "")).strip()
        roi_name = str(row.get("roi_name", "")).strip()
        if not label:
            raise RegionalNullStressError("regional null requires a non-empty region_label")
        if label.casefold() == roi_name.casefold() or re.fullmatch(r"roi_[0-9]+", label, flags=re.IGNORECASE):
            raise RegionalNullStressError("region_label cannot be inferred from ROI name")
        if row.get("evidence_kind") not in {"direct_region", "manual_region"}:
            raise RegionalNullStressError("regional null requires direct_region or manual_region evidence")
        if not str(row.get("notes", "")).strip():
            raise RegionalNullStressError("regional null requires provenance notes")


def run_case(
    name: str,
    rows: list[list[str]],
    expected: str,
    regional_gate: bool = False,
    expected_pairs: tuple[tuple[str, str], ...] = EXPECTED_PAIRS,
) -> dict[str, Any]:
    """Run one accepted or rejected contract case and record its raw outcome."""
    with tempfile.TemporaryDirectory(prefix="h4-regional-null-") as directory:
        root = Path(directory)
        annotations = root / "annotations.tsv"
        mapping = root / "mapping.tsv"
        write_tsv(annotations, ANNOTATION_HEADER, annotations_rows())
        write_tsv(mapping, MAPPING_HEADER, rows)
        try:
            manifest = build_manifest(mapping, annotations, expected_pairs)
            if regional_gate:
                evaluate_regional_input(manifest)
            observed = "ACCEPTED"
            detail: dict[str, Any] = {
                "mapping_verdict": manifest.get("mapping_verdict"),
                "row_count": manifest.get("counts", {}).get("row_count"),
            }
        except (OSError, csv.Error, RoiCompartmentError, RegionalNullStressError, ValueError) as exc:
            observed = "REJECTED"
            detail = {"error": str(exc)}
        return {
            "name": name,
            "expected": expected,
            "observed": observed,
            "pass": observed == expected,
            "detail": detail,
        }


def public_manifest_gate(path: Path) -> dict[str, Any]:
    """Verify that the current public manifest cannot enter a regional null."""
    data = json.loads(path.read_text(encoding="utf-8"))
    counts = data.get("counts", {})
    mapping_verdict = data.get("mapping_verdict")
    accepted = mapping_verdict == "REGIONAL" and counts.get("region_rows") == counts.get("row_count") and counts.get("row_count", 0) > 0
    return {
        "name": "current_public_r65d11_manifest",
        "expected": "REJECTED",
        "observed": "ACCEPTED" if accepted else "REJECTED",
        "pass": not accepted,
        "detail": {
            "mapping_verdict": mapping_verdict,
            "counts": counts,
            "reason": "no explicit REGION_MAPPED rows are present; biological regional null not run",
        },
    }


def main(argv: list[str] | None = None) -> int:
    """Run the regional-null boundary stress matrix and emit a JSON receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    unmapped_rows = [valid_unmapped_row("ROI_0"), valid_unmapped_row("ROI_1")]
    missing_region = [row.copy() for row in valid_region_rows()]
    missing_region[0][5] = ""
    roi_name_region = [row.copy() for row in valid_region_rows()]
    roi_name_region[0][5] = "ROI_0"
    dff_only = [row.copy() for row in valid_region_rows()]
    dff_only[0][8] = "dff_correlation"
    unmapped_with_region = [row.copy() for row in unmapped_rows]
    unmapped_with_region[0][5] = "central_complex"
    invalid_weights = [
        ["fly1", "1", "ROI_0", "POPULATION", "POPULATION_MAPPED", "", "101;202", "0.2;0.2", "manual_population", "0.7", "bad weights"],
        valid_unmapped_row("ROI_1"),
    ]
    unknown_root = [
        ["fly1", "1", "ROI_0", "POPULATION", "POPULATION_MAPPED", "", "999;202", "0.5;0.5", "manual_population", "0.7", "unknown root"],
        valid_unmapped_row("ROI_1"),
    ]
    missing_pair = [valid_unmapped_row("ROI_0")]
    duplicate_pair = [valid_unmapped_row("ROI_0"), valid_unmapped_row("ROI_0")]
    cases = [
        public_manifest_gate(args.public_manifest),
        run_case("valid_explicit_region", valid_region_rows(), "ACCEPTED", regional_gate=True),
        run_case("missing_region_label", missing_region, "REJECTED"),
        run_case("roi_name_used_as_region", roi_name_region, "REJECTED", regional_gate=True),
        run_case("dff_only_region_evidence", dff_only, "REJECTED"),
        run_case("unmapped_row_with_region", unmapped_with_region, "REJECTED"),
        run_case("population_weights_not_normalized", invalid_weights, "REJECTED"),
        run_case("population_root_absent_from_annotations", unknown_root, "REJECTED"),
        run_case("missing_trial_roi_pair", missing_pair, "REJECTED"),
        run_case("duplicate_trial_roi_pair", duplicate_pair, "REJECTED"),
    ]
    passed = sum(case["pass"] for case in cases)
    receipt = {
        "schema": "h4-regional-null-stress/v1",
        "stress_verdict": "PASS_FAIL_CLOSED" if passed == len(cases) else "MAL",
        "biological_regional_null": "NO_MEDIDO",
        "biological_reason": "the public R65D11 manifest has 0 REGION_MAPPED rows and cannot support an anatomical regional null",
        "case_count": len(cases),
        "passed_cases": passed,
        "failed_cases": len(cases) - passed,
        "cases": cases,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"stress_verdict": receipt["stress_verdict"], "biological_regional_null": receipt["biological_regional_null"], "case_count": len(cases), "passed_cases": passed, "failed_cases": len(cases) - passed, "out": str(args.out)}, sort_keys=True))
    return 0 if receipt["stress_verdict"] == "PASS_FAIL_CLOSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
