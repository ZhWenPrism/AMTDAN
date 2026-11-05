import unittest

from amtdan.evaluation.metrics import ordinal_metrics

try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipUnless(np is not None, "NumPy is optional")
class UnsignedGradesTests(unittest.TestCase):
    def test_unsigned_grades_match_python_integers(self):
        truth, predicted = [0, 3, 4], [1, 4, 2]
        observed = ordinal_metrics(np.asarray(truth, dtype=np.uint8),
                                   np.asarray(predicted, dtype=np.uint8))
        self.assertEqual(observed, ordinal_metrics(truth, predicted))
