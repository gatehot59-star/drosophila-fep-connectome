#!/usr/bin/env python3
"""Contracts for temporal-half stability."""
from __future__ import annotations

import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from h4_temporal_halves import TemporalHalvesError, _shuffle_labels, analyze_trials, balanced_accuracy  # noqa: E402


def write_trial(path: Path, animal: str, trial: str, legacy_frame: bool = False) -> None:
    """Write a compact two-label aligned feature fixture."""
    labels = ["walking", "walking", "resting", "resting", "walking", "walking", "resting", "resting"]
    rows = []
    previous = None
    bout_id = -1
    position = 0
    for index, label in enumerate(labels):
        if label != previous:
            bout_id += 1
            position = 0
            previous = label
        row = {"record_type": "frame", "animal": animal, "trial": trial, "behavior_frame": index, "time_s": float(index), "label": label, "context": "co2_off", "bout_id": bout_id, "bout_position": position, "bout_length": 2, "roi": {"ROI_0": 4.0 if label == "walking" else -4.0, "ROI_1": float(index)}}
        if legacy_frame:
            row["Frame"] = index
        rows.append(row)
        position += 1
    metadata = {"record_type": "metadata", "schema": "h4-aligned-features/v1", "verdict": "BIEN", "identity": {"animal": animal, "trial": trial, "timebase": "thor_sync_seconds"}, "roi_names": ["ROI_0", "ROI_1"], "n_records": len(rows)}
    path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in [metadata, *rows]), encoding="utf-8")


class TemporalHalvesTests(unittest.TestCase):
    """Exercise split, identity and repeatability contracts."""

    def test_rejects_legacy_frame(self):
        """Historical Frame joins are forbidden."""
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"t{i}.jsonl" for i in range(3)]
            write_trial(paths[0], "fly1", "1", legacy_frame=True)
            write_trial(paths[1], "fly1", "2")
            write_trial(paths[2], "fly1", "3")
            with self.assertRaisesRegex(TemporalHalvesError, "legacy Frame"):
                analyze_trials(paths, permutations=3)

    def test_rejects_mixed_animals(self):
        """A within-animal stability instrument refuses mixed animals."""
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"t{i}.jsonl" for i in range(3)]
            write_trial(paths[0], "fly1", "1")
            write_trial(paths[1], "fly1", "2")
            write_trial(paths[2], "fly2", "3")
            with self.assertRaisesRegex(TemporalHalvesError, "multiple animals"):
                analyze_trials(paths, permutations=3)

    def test_reproducible_and_bouts_are_not_split(self):
        """Same seed repeats, and each half contains complete two-frame bouts."""
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"t{i}.jsonl" for i in range(3)]
            for index, path in enumerate(paths):
                write_trial(path, "fly1", str(index + 1))
            first = analyze_trials(paths, permutations=7, seed=19)
            second = analyze_trials(paths, permutations=7, seed=19)
            self.assertEqual(first, second)
            self.assertEqual(len(first["pooled"]["null_scores"]), 7)
            for trial in first["trials"]:
                self.assertEqual(trial["early_frames"] % 2, 0)
                self.assertEqual(trial["late_frames"] % 2, 0)

    def test_balanced_accuracy_is_bounded(self):
        """The directional score remains in [0,1]."""
        observations = [{"label": "walking", "vector": (1.0,)}, {"label": "resting", "vector": (-1.0,)}]
        score = balanced_accuracy(observations, {"walking": (1.0,), "resting": (-1.0,)}, ("walking", "resting"))
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_null_preserves_tokens_inside_each_segment(self):
        """The null cannot move labels across segments or alter slot data."""
        observations = [
            {"segment": 0, "label": "walking", "length": 2, "vector": (1.0,)},
            {"segment": 0, "label": "resting", "length": 3, "vector": (-1.0,)},
            {"segment": 1, "label": "walking", "length": 4, "vector": (2.0,)},
            {"segment": 1, "label": "resting", "length": 5, "vector": (-2.0,)},
        ]
        shuffled = _shuffle_labels(observations, seed=19)
        for segment in (0, 1):
            before_labels = Counter(item["label"] for item in observations if item["segment"] == segment)
            after_labels = Counter(item["label"] for item in shuffled if item["segment"] == segment)
            self.assertEqual(before_labels, after_labels)
        self.assertEqual([item["length"] for item in shuffled], [item["length"] for item in observations])
        self.assertEqual([item["vector"] for item in shuffled], [item["vector"] for item in observations])


if __name__ == "__main__":
    unittest.main()
