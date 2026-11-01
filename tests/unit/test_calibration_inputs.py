import unittest
from math import nan

from amtdan.evaluation import expected_calibration_error


class CalibrationInputsTest(unittest.TestCase):
    def test_non_binary_correctness_is_rejected(self):
        for value in (2, -1, nan, None, "1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                expected_calibration_error([value], [0.8])

    def test_invalid_bin_counts_raise_value_error(self):
        for bins in (True, 1.5, 0, -1):
            with self.subTest(bins=bins), self.assertRaises(ValueError):
                expected_calibration_error([1], [0.8], bins=bins)

    def test_binary_values_and_confidence_boundaries_are_unchanged(self):
        self.assertEqual(expected_calibration_error([False, True], [0.0, 1.0], bins=2), 0.0)

    def test_numpy_sequences_are_accepted_when_available(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest("NumPy is optional")
        self.assertAlmostEqual(expected_calibration_error(np.array([1, 0]), np.array([0.9, 0.8]), bins=2), 0.35)

