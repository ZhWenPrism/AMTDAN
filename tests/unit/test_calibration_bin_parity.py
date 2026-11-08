import math
import random
import unittest

from amtdan.evaluation import expected_calibration_error


class CalibrationBinParityTest(unittest.TestCase):
    def test_edges_and_adjacent_floats_match_reference_bins(self):
        rng = random.Random(30)
        for bins in (1, 3, 7, 10, 50):
            edges = [i / bins for i in range(1, bins)]
            confidence = [0.0, 1.0] + [rng.random() for _ in range(200)]
            for edge in edges:
                confidence.extend((math.nextafter(edge, 0.0), edge, math.nextafter(edge, 1.0)))
            correctness = [rng.randrange(2) for _ in confidence]
            reference = 0.0
            for i in range(bins):
                pairs = [(c, p) for c, p in zip(correctness, confidence)
                         if i / bins <= p < (i + 1) / bins or (i == bins - 1 and p == 1)]
                if pairs:
                    n = len(pairs)
                    reference += n / len(confidence) * abs(
                        sum(c for c, _ in pairs) / n - sum(p for _, p in pairs) / n
                    )
            with self.subTest(bins=bins):
                self.assertAlmostEqual(expected_calibration_error(correctness, confidence, bins), reference, places=14)
