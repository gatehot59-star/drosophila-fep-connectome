#!/usr/bin/env python3
"""Contract tests for the H4 block-preserving null instrument."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from h4_block_null import (  # noqa: E402
    BlockNullError,
    analyze_trials,
    eta_squared,
    load_trial,
    token_observations,
)


def _write_trial(path: Path, animal: str = "fly1", include_frame: bool = False) -> None:
    """Write a compact valid aligned-features fixture."""
    labels = ["walking", "walking", "resting", "resting", "walking", "walking"]
    lengths = {"walking": 2, "resting": 2}
    rows = []
    bout_id = -1
    previous = None
    position = 0
    for index, label in enumerate(labels):
        if label != previous:
            bout_id += 1
            position = 0
            previous = label
        row = {
            "record_type": "frame", "animal": animal, "trial": "1", "behavior_frame": index,
            "time_s": float(index), "label": label, "context": "co2_off", "bout_id": bout_id,
            "bout_position": position, "bout_length": lengths[label],
            "roi": {"ROI_0": 10.0 if label == "walking" else 0.0, "ROI_1": float(index)},
        }
        if include_frame:
            row["Frame"] = index
        rows.append(row)
        position += 1
    metadata = {
        "record_type": "metadata", "schema": "h4-aligned-features/v1", "verdict": "BIEN",
        "identity": {"animal": animal, "trial": "1", "timebase": "thor_sync_seconds"},
        "roi_names": ["ROI_0", "ROI_1"], "n_records": len(rows),
    }
    path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in [metadata, *rows]), encoding="utf-8")


class H4BlockNullTests(unittest.TestCase):
    """Exercise positive, negative, preservation and reproducibility contracts."""

    def test_rejects_legacy_frame_join_field(self):
        """The null cannot accept the historical incompatible join key."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trial.jsonl"
            _write_trial(path, include_frame=True)
            with self.assertRaisesRegex(BlockNullError, "legacy Frame"):
                load_trial(path)

    def test_rejects_multiple_animals_by_default(self):
        """The within-animal instrument refuses a mislabeled cross-animal claim."""
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first.jsonl", Path(directory) / "second.jsonl"
            _write_trial(first, animal="fly1")
            _write_trial(second, animal="fly2")
            with self.assertRaisesRegex(BlockNullError, "multiple animals"):
                analyze_trials([first, second], permutations=5)

    def test_eta_score_is_bounded_and_uses_bout_observations(self):
        """The descriptive statistic is finite and bounded by one."""
        observations = [("a", (1.0, 0.0)), ("a", (1.1, 0.0)), ("b", (-1.0, 0.0)), ("b", (-1.1, 0.0))]
        score, means, counts = eta_squared(observations, ["a", "b"], min_bouts=2)
        self.assertGreater(score, 0.9)
        self.assertLessEqual(score, 1.0)
        self.assertEqual(counts, {"a": 2, "b": 2})
        self.assertEqual(set(means), {"a", "b"})

    def test_analysis_is_reproducible_and_preserves_block_contract(self):
        """Identical seed and input produce identical nulls and preservation counts."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trial.jsonl"
            _write_trial(path)
            first = analyze_trials([path], permutations=20, seed=17)
            second = analyze_trials([path], permutations=20, seed=17)
            self.assertEqual(first, second)
            trial = first["trial_results"][0]
            self.assertEqual(trial["preservation"]["label_frame_counts"], {"resting": 2, "walking": 4})
            self.assertEqual(trial["preservation"]["label_bout_counts"], {"resting": 1, "walking": 2})
            self.assertEqual(len(first["pooled"]["null_scores"]), 20)

    def test_token_observations_rejects_wrong_block_lengths(self):
        """A permutation that loses a frame cannot pass as a valid null."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trial.jsonl"
            _write_trial(path)
            trial = load_trial(path)
            module = __import__("h4_block_null")
            segments = module._normalized(trial)
            with self.assertRaisesRegex(BlockNullError, "do not cover"):
                token_observations(segments, [[type(segments[0].tokens[0])("walking", 1)]])


if __name__ == "__main__":
    unittest.main()
