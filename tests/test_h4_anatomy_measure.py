#!/usr/bin/env python3
"""Tests for quantitative confocal anatomy measurement primitives."""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from h4_anatomy_measure import AnatomyMeasureError, otsu_threshold  # noqa: E402


class AnatomyMeasureTests(unittest.TestCase):
    """Exercise thresholding and input guards without shipping image data."""

    def test_otsu_separates_two_intensity_modes(self):
        """A bimodal histogram receives a threshold between the modes."""
        histogram = [0] * 256
        histogram[10] = 1000
        histogram[200] = 1000
        threshold = otsu_threshold(histogram)
        self.assertGreaterEqual(threshold, 10)
        self.assertLess(threshold, 200)

    def test_otsu_rejects_empty_histogram(self):
        """An empty histogram cannot produce an anatomical threshold."""
        with self.assertRaisesRegex(AnatomyMeasureError, "256 non-empty"):
            otsu_threshold([0] * 256)

    def test_otsu_rejects_wrong_histogram_shape(self):
        """The instrument requires the declared 8-bit intensity domain."""
        with self.assertRaisesRegex(AnatomyMeasureError, "256"):
            otsu_threshold([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
