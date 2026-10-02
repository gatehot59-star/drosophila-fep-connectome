#!/usr/bin/env python3
"""Tests for the official H4 loader contracts."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from h4_alignment_guard import AlignmentError, validate_temporal_alignment
from h4_official_loader import validate_dff_lengths


class H4OfficialLoaderTests(unittest.TestCase):
    """Ensure the loader rejects the failure modes that invalidated H4."""

    def test_accepts_equal_roi_lengths(self):
        """Equal ROI arrays are accepted."""
        self.assertEqual(
            validate_dff_lengths({"ROI_0": [1, 2], "ROI_1": [3, 4]}, 2),
            {"ROI_0": 2, "ROI_1": 2},
        )

    def test_rejects_truncated_roi(self):
        """A truncated ROI cannot be silently interpolated."""
        with self.assertRaisesRegex(ValueError, "DFF length mismatch"):
            validate_dff_lengths({"ROI_0": [1, 2], "ROI_1": [3]}, 2)

    def test_rejects_empty_dff(self):
        """A manifest with no ROI arrays is invalid."""
        with self.assertRaisesRegex(ValueError, "no ROI"):
            validate_dff_lengths({}, 2)

    def test_rejects_frame_join(self):
        """The historical integer-frame join is forbidden."""
        with self.assertRaisesRegex(AlignmentError, "unsafe"):
            validate_temporal_alignment(
                [0.0, 1.0, 2.0],
                [0.0, 1.0, 2.0],
                neural_metadata={"animal": "Fly1", "trial": "007", "timebase": "thor_sync_seconds"},
                behavior_metadata={"animal": "Fly1", "trial": "007", "timebase": "thor_sync_seconds"},
                join_key="Frame",
            )

    def test_rejects_mismatched_identity(self):
        """A neural and behavior source from different animals cannot join."""
        with self.assertRaisesRegex(AlignmentError, "identity mismatch"):
            validate_temporal_alignment(
                [0.0, 1.0, 2.0],
                [0.0, 1.0, 2.0],
                neural_metadata={"animal": "Fly1", "trial": "007", "timebase": "thor_sync_seconds"},
                behavior_metadata={"animal": "Fly2", "trial": "007", "timebase": "thor_sync_seconds"},
            )

    def test_rejects_clock_gap(self):
        """A large internal gap is rejected after duration has passed."""
        with self.assertRaisesRegex(AlignmentError, "gap"):
            validate_temporal_alignment(
                [0.0, 0.01, 0.02, 0.03, 1.03, 2.0],
                [0.0, 1.0, 2.0],
                neural_metadata={"animal": "Fly1", "trial": "007", "timebase": "thor_sync_seconds"},
                behavior_metadata={"animal": "Fly1", "trial": "007", "timebase": "thor_sync_seconds"},
            )


if __name__ == "__main__":
    unittest.main()
