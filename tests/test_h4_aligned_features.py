#!/usr/bin/env python3
"""Contract tests for ROI-preserving aligned H4 features."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from h4_aligned_features import (  # noqa: E402
    FeatureAlignmentError,
    derive_bouts,
    frame_records,
    interpolate_series,
)


class H4AlignedFeaturesTests(unittest.TestCase):
    """Exercise valid records and the failure modes that would falsify them."""

    def test_interpolates_linear_roi_without_extrapolation(self):
        """A linear signal is reconstructed exactly at an interior time."""
        result = interpolate_series([0.0, 1.0, 2.0], [0.0, 2.0, 4.0], [0.5, 1.5])
        self.assertEqual(result, [1.0, 3.0])

    def test_rejects_target_outside_neural_coverage(self):
        """The feature path refuses endpoint extrapolation."""
        with self.assertRaisesRegex(FeatureAlignmentError, "extrapolation"):
            interpolate_series([0.0, 1.0], [1.0, 2.0], [-0.1, 0.5])

    def test_rejects_roi_length_mismatch(self):
        """An ROI with a missing aligned row cannot silently disappear."""
        with self.assertRaisesRegex(FeatureAlignmentError, "row-count"):
            frame_records(
                animal="fly1",
                trial="7",
                times=[0.0, 1.0],
                labels=["walking", "resting"],
                contexts=["co2_off", "co2_off"],
                roi_features={"ROI_0": [0.1]},
            )

    def test_bout_breaks_on_label_or_context(self):
        """A block changes at an action transition or context transition."""
        bouts = derive_bouts(
            ["walking", "walking", "walking", "walking"],
            ["co2_off", "co2_off", "co2_on", "co2_on"],
        )
        self.assertEqual([row["bout_id"] for row in bouts], [0, 0, 1, 1])
        self.assertEqual([row["bout_length"] for row in bouts], [2, 2, 2, 2])
        self.assertEqual([row["bout_position"] for row in bouts], [0, 1, 0, 1])

    def test_records_keep_roi_identity_and_action_flag(self):
        """Rows expose named ROI values instead of a collapsed global statistic."""
        rows = frame_records(
            animal="fly1",
            trial="7",
            times=[0.0, 1.0],
            labels=["walking", "background"],
            contexts=["co2_off", "co2_off"],
            roi_features={"ROI_1": [0.2, 0.3], "ROI_0": [0.1, 0.4]},
        )
        self.assertEqual(rows[0]["roi"], {"ROI_0": 0.1, "ROI_1": 0.2})
        self.assertTrue(rows[0]["is_action"])
        self.assertFalse(rows[1]["is_action"])
        self.assertEqual(rows[1]["bout_id"], 1)

    def test_rejects_mismatched_labels_and_contexts(self):
        """The block structure cannot be invented from unequal arrays."""
        with self.assertRaisesRegex(FeatureAlignmentError, "equal length"):
            derive_bouts(["walking"], [])


if __name__ == "__main__":
    unittest.main()
