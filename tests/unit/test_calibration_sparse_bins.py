import tracemalloc
import unittest
from amtdan.evaluation.metrics import expected_calibration_error


class SparseCalibrationBinsTest(unittest.TestCase):
    def test_memory_tracks_occupied_bins_rather_than_requested_bins(self):
        expected_calibration_error([1, 0], [.9, .8], bins=3)
        tracemalloc.start()
        try:
            result = expected_calibration_error([1, 0], [.9, .8], bins=200001)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertLess(peak, 2_000_000)
        self.assertAlmostEqual(result, .45)

    def test_aggregation_and_endpoint_bins_keep_the_existing_definition(self):
        self.assertAlmostEqual(expected_calibration_error([1, 0], [.9, .8], bins=1), .35)
        self.assertAlmostEqual(expected_calibration_error([1, 0], [.9, .8], bins=10), .45)
        self.assertAlmostEqual(expected_calibration_error([1, 0, 1], [0., .5, 1.], bins=200001), .5)
