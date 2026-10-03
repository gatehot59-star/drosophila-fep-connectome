#!/usr/bin/env python3
"""Contracts for within-animal leave-one-trial-out H4 generalization."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from h4_trial_generalization import BlockNullError, Observation, analyze_trials, balanced_accuracy  # noqa: E402


def write_trial(path: Path, animal: str, trial: str, legacy_frame: bool = False) -> None:
    """Write a compact fixture with both target labels and complete bouts."""
    labels = ["walking", "walking", "resting", "resting", "walking", "walking"]
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


class GeneralizationTests(unittest.TestCase):
    """Exercise classifier, identity guards and reproducibility."""

    def test_balanced_accuracy_perfect_centroids(self):
        """The score reaches one when class centroids separate the observations."""
        observations = [Observation("walking", (1.0, 0.0), 2, 0, 0), Observation("resting", (-1.0, 0.0), 2, 0, 1)]
        self.assertEqual(balanced_accuracy(observations, {"walking": (1.0, 0.0), "resting": (-1.0, 0.0)}, ("resting", "walking")), 1.0)

    def test_rejects_legacy_frame(self):
        """The historical incompatible join key fails closed through the loader."""
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"t{i}.jsonl" for i in range(3)]
            write_trial(paths[0], "fly1", "1", legacy_frame=True)
            write_trial(paths[1], "fly1", "2")
            write_trial(paths[2], "fly1", "3")
            with self.assertRaisesRegex(BlockNullError, "legacy Frame"):
                analyze_trials(paths, permutations=3)

    def test_rejects_mixed_animals(self):
        """The within-animal instrument cannot be mislabeled cross-animal."""
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"t{i}.jsonl" for i in range(3)]
            for index, path in enumerate(paths):
                write_trial(path, "fly1" if index < 2 else "fly2", str(index + 1))
            with self.assertRaisesRegex(BlockNullError, "multiple animals"):
                analyze_trials(paths, permutations=3)

    def test_result_is_reproducible_and_has_pooled_null(self):
        """Same input and seed yield identical folds and null distribution."""
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"t{i}.jsonl" for i in range(3)]
            for index, path in enumerate(paths):
                write_trial(path, "fly1", str(index + 1))
            first = analyze_trials(paths, permutations=7, seed=19)
            second = analyze_trials(paths, permutations=7, seed=19)
            self.assertEqual(first, second)
            self.assertEqual(first["analysis"]["cross_animal"], False)
            self.assertEqual(len(first["pooled"]["null_scores"]), 7)
            self.assertEqual(len(first["folds"]), 3)


if __name__ == "__main__":
    unittest.main()
