import unittest

from amtdan.datasets import ExaminationRecord, ModalityState
from amtdan.evaluation import ordinal_metrics


class SeverityTypeTest(unittest.TestCase):
    def test_non_integer_grades_are_rejected_by_records(self):
        for grade in (True, False, 1.0, "1"):
            with self.subTest(grade=grade), self.assertRaises(ValueError):
                ExaminationRecord(
                    "sample", "exam", "site", ModalityState(True, False),
                    severity_labels={"task": grade},
                )

    def test_boolean_grades_are_rejected_by_metrics(self):
        for truth, predicted in (([True], [1]), ([1], [True])):
            with self.subTest(truth=truth, predicted=predicted), self.assertRaises(ValueError):
                ordinal_metrics(truth, predicted)
