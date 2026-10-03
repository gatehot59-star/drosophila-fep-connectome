#!/usr/bin/env python3
"""Validate an explicit ROI-to-FlyWire anatomy mapping without inference."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA = "h4-roi-anatomy-map/v1"
MAPPING_COLUMNS = ("roi_name", "root_id", "mapping_status", "evidence_kind", "confidence", "notes")
ANNOTATION_COLUMNS = ("root_id", "super_class", "cell_class", "flow", "supertype", "cell_type", "top_nt", "top_nt_conf", "side")
MAPPED_EVIDENCE = frozenset({"direct_root_id", "manual_roi_to_cell"})


class RoiAnatomyError(ValueError):
    """Raised when an ROI anatomy manifest is incomplete or unsafe."""


def md5_file(path: Path) -> str:
    """Return the MD5 used by the pinned FlyWire provenance manifests."""
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _root_id(value: str, field: str) -> int:
    """Parse a positive FlyWire root ID."""
    token = value.strip()
    if not token or token.upper() in {"NA", "NONE", "NULL"}:
        raise RoiAnatomyError(f"{field}: root_id is required")
    try:
        parsed = int(token)
    except ValueError as exc:
        raise RoiAnatomyError(f"{field}: root_id is not an integer") from exc
    if parsed <= 0:
        raise RoiAnatomyError(f"{field}: root_id must be positive")
    return parsed


def _confidence(value: str, field: str) -> float:
    """Parse a finite confidence in the closed interval [0, 1]."""
    try:
        parsed = float(value)
    except ValueError as exc:
        raise RoiAnatomyError(f"{field}: confidence is not numeric") from exc
    if not math.isfinite(parsed) or not 0.0 <= parsed <= 1.0:
        raise RoiAnatomyError(f"{field}: confidence must be finite and between 0 and 1")
    return parsed


def _required_columns(fieldnames: Sequence[str] | None, required: Sequence[str], name: str) -> None:
    """Require a tabular contract before reading any rows."""
    if fieldnames is None:
        raise RoiAnatomyError(f"{name}: missing header")
    missing = sorted(set(required) - set(fieldnames))
    if missing:
        raise RoiAnatomyError(f"{name}: missing columns {missing}")


def load_annotations(path: Path) -> dict[int, dict[str, str]]:
    """Load and uniquely index the pinned annotation snapshot by root ID."""
    if not path.is_file():
        raise RoiAnatomyError(f"annotations file does not exist: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        _required_columns(reader.fieldnames, ANNOTATION_COLUMNS, "annotations")
        output: dict[int, dict[str, str]] = {}
        for line_number, row in enumerate(reader, start=2):
            raw_root = (row.get("root_id") or "").strip()
            if not raw_root:
                raise RoiAnatomyError(f"annotations line {line_number}: empty root_id")
            root = _root_id(raw_root, f"annotations line {line_number}")
            if root in output:
                raise RoiAnatomyError(f"annotations line {line_number}: duplicate root_id {root}")
            output[root] = {column: (row.get(column) or "").strip() for column in ANNOTATION_COLUMNS if column != "root_id"}
    if not output:
        raise RoiAnatomyError("annotations: no rows")
    return output


def load_mapping(path: Path, expected_rois: Sequence[str]) -> list[dict[str, Any]]:
    """Load one explicit mapping row for every expected ROI name."""
    if not path.is_file():
        raise RoiAnatomyError(f"mapping file does not exist: {path}")
    expected = tuple(expected_rois)
    if not expected or len(set(expected)) != len(expected):
        raise RoiAnatomyError("expected ROI names must be non-empty and unique")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        _required_columns(reader.fieldnames, MAPPING_COLUMNS, "mapping")
        rows: list[dict[str, Any]] = []
        seen: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            name = (row.get("roi_name") or "").strip()
            if not name:
                raise RoiAnatomyError(f"mapping line {line_number}: empty roi_name")
            if name in seen:
                raise RoiAnatomyError(f"mapping line {line_number}: duplicate roi_name {name}")
            seen.add(name)
            status = (row.get("mapping_status") or "").strip().upper()
            evidence = (row.get("evidence_kind") or "").strip()
            notes = (row.get("notes") or "").strip()
            if status not in {"MAPPED", "UNMAPPED"}:
                raise RoiAnatomyError(f"mapping line {line_number}: mapping_status must be MAPPED or UNMAPPED")
            confidence = _confidence((row.get("confidence") or ""), f"mapping line {line_number}")
            root: int | None
            raw_root = (row.get("root_id") or "").strip()
            if status == "MAPPED":
                if evidence not in MAPPED_EVIDENCE:
                    raise RoiAnatomyError(f"mapping line {line_number}: mapped ROI needs direct or manual cell evidence")
                root = _root_id(raw_root, f"mapping line {line_number}")
                if not notes:
                    raise RoiAnatomyError(f"mapping line {line_number}: mapped ROI needs provenance notes")
            else:
                if raw_root not in {"", "NA", "NONE", "NULL"} or evidence != "unmapped" or confidence != 0.0:
                    raise RoiAnatomyError(f"mapping line {line_number}: UNMAPPED rows must have empty root_id, unmapped evidence and confidence 0")
                root = None
            rows.append({"roi_name": name, "root_id": root, "mapping_status": status, "evidence_kind": evidence, "confidence": confidence, "notes": notes})
    if set(expected) != seen:
        raise RoiAnatomyError(f"mapping ROI set differs: expected {sorted(expected)}, got {sorted(seen)}")
    return [next(row for row in rows if row["roi_name"] == name) for name in expected]


def build_manifest(mapping_path: Path, annotations_path: Path, expected_rois: Sequence[str]) -> dict[str, Any]:
    """Validate an explicit mapping and join only by declared FlyWire root IDs."""
    annotations = load_annotations(annotations_path)
    rows = load_mapping(mapping_path, expected_rois)
    mapped_roots: set[int] = set()
    output_rows: list[dict[str, Any]] = []
    for row in rows:
        root = row["root_id"]
        annotation: dict[str, str] = {}
        if root is not None:
            if root not in annotations:
                raise RoiAnatomyError(f"{row['roi_name']}: root_id {root} is absent from annotation snapshot")
            if root in mapped_roots:
                raise RoiAnatomyError(f"{row['roi_name']}: root_id {root} is assigned to more than one ROI")
            mapped_roots.add(root)
            annotation = annotations[root]
        output_rows.append({**row, "annotation": annotation})
    mapped = sum(row["mapping_status"] == "MAPPED" for row in rows)
    mapping_verdict = "COMPLETE" if mapped == len(rows) else ("PARTIAL" if mapped else "NO_MAPPED_ROIS")
    return {
        "schema": SCHEMA,
        "verdict": "BIEN",
        "mapping_verdict": mapping_verdict,
        "expected_roi_names": list(expected_rois),
        "counts": {"roi_count": len(rows), "mapped_rois": mapped, "unmapped_rois": len(rows) - mapped, "annotation_rows": len(annotations)},
        "inputs": {"mapping": {"path": str(mapping_path), "bytes": mapping_path.stat().st_size, "md5": md5_file(mapping_path)}, "annotations": {"path": str(annotations_path), "bytes": annotations_path.stat().st_size, "md5": md5_file(annotations_path)}},
        "rois": output_rows,
        "limitations": ["This manifest validates declared evidence; it never infers anatomy from ROI signal or ROI index.", "A PARTIAL or NO_MAPPED_ROIS manifest cannot support an anatomical H4 claim.", "Annotation membership does not establish causal route identity."],
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Validate a mapping TSV and write a provenance manifest."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--roi", dest="rois", action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest(args.mapping, args.annotations, args.rois)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"verdict": manifest["verdict"], "mapping_verdict": manifest["mapping_verdict"], "counts": manifest["counts"], "out": str(args.out)}, sort_keys=True))
        return 0
    except (OSError, csv.Error, RoiAnatomyError, ValueError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
