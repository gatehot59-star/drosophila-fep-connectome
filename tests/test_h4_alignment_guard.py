#!/usr/bin/env python3
"""Tests for the fail-closed H4 alignment guard."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from h4_alignment_guard import AlignmentError, validate_temporal_alignment


class H4AlignmentGuardTests(unittest.TestCase):
    """Exercise both accepted and rejected alignment contracts."""

    def metadata(self, *, timebase="camera_seconds"):
        return {"animal": "Fly1", "trial": "007", "timebase": timebase}

    def test_valid_time_alignment(self):
        report = validate_temporal_alignment(
            [0.0, 1.0, 2.0, 3.0],
            [0.01, 1.01, 2.01, 3.01],
            neural_metadata=self.metadata(),
            behavior_metadata=self.metadata(),
        )
        self.assertEqual(report["verdict"], "BIEN")
        self.assertGreater(report["coverage_neural"], 0.99)

    def test_rejects_frame_join(self):
        with self.assertRaisesRegex(AlignmentError, "not.*Frame"):
            validate_temporal_alignment(
                [0.0, 1.0, 2.0],
                [0.0, 1.0, 2.0],
                neural_metadata=self.metadata(),
                behavior_metadata=self.metadata(),
                join_key="Frame",
            )

    def test_rejects_clock_identity_mismatch(self):
        with self.assertRaisesRegex(AlignmentError, "timebase"):
            validate_temporal_alignment(
                [0.0, 1.0, 2.0],
                [0.0, 1.0, 2.0],
                neural_metadata=self.metadata(timebase="two_photon_frame_time"),
                behavior_metadata=self.metadata(timebase="camera_frame_100hz"),
            )

    def test_rejects_missing_identity(self):
        with self.assertRaisesRegex(AlignmentError, "missing identity"):
            validate_temporal_alignment(
                [0.0, 1.0, 2.0],
                [0.0, 1.0, 2.0],
                neural_metadata={"animal": "Fly1", "trial": "007"},
                behavior_metadata=self.metadata(),
            )

    def test_rejects_non_monotonic_axis(self):
        with self.assertRaisesRegex(AlignmentError, "strictly increasing"):
            validate_temporal_alignment(
                [0.0, 2.0, 1.0],
                [0.0, 1.0, 2.0],
                neural_metadata=self.metadata(),
                behavior_metadata=self.metadata(),
            )

    def test_rejects_duration_mismatch(self):
        with self.assertRaisesRegex(AlignmentError, "duration mismatch"):
            validate_temporal_alignment(
                [0.0, 1.0, 2.0],
                [0.0, 3.0, 6.0],
                neural_metadata=self.metadata(),
                behavior_metadata=self.metadata(),
            )

    def test_rejects_insufficient_overlap(self):
        with self.assertRaisesRegex(AlignmentError, "overlap"):
            validate_temporal_alignment(
                [0.0, 1.0, 2.0],
                [10.0, 11.0, 12.0],
                neural_metadata=self.metadata(),
                behavior_metadata=self.metadata(),
            )


if __name__ == "__main__":
    unittest.main()
