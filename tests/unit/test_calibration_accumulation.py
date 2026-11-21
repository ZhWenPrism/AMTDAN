from decimal import Decimal
import unittest

from amtdan.evaluation import expected_calibration_error


class CalibrationAccumulationTest(unittest.TestCase):
    def test_decimal_confidence_matches_float_confidence(self):
        self.assertAlmostEqual(expected_calibration_error([1, 0], [Decimal("0.75"), Decimal("0.25")]), 0.25)

    def test_half_precision_confidence_does_not_saturate_the_bin_sum(self):
        import numpy as np
        confidence = np.ones(4096, dtype=np.float16)
        self.assertEqual(expected_calibration_error([1] * len(confidence), confidence), 0.0)
