import unittest
from enum import IntEnum

from amtdan.evaluation import ordinal_metrics


class OrdinalInputTests(unittest.TestCase):
    def test_invalid_class_counts_raise_value_error(self):
        for classes in (0, 1, -1, 2.5, True, float("nan")):
            with self.subTest(classes=classes), self.assertRaises(ValueError):
                ordinal_metrics([0], [0], classes=classes)

    def test_float_labels_are_rejected_before_matrix_indexing(self):
        for truth, prediction in (([0.0, 1.0], [0, 1]), ([0, 1], [0.0, 1.0])):
            with self.subTest(truth=truth, prediction=prediction):
                with self.assertRaises(ValueError):
                    ordinal_metrics(truth, prediction)

    def test_integer_enums_and_generators_remain_supported(self):
        class Grade(IntEnum):
            LOW = 0
            HIGH = 1

        result = ordinal_metrics(iter([Grade.LOW, Grade.HIGH]), iter([0, 1]), classes=2)
        self.assertEqual(result.accuracy, 1.0)
        self.assertEqual(result.confusion_matrix, ((1, 0), (0, 1)))
