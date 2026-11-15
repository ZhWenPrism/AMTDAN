import unittest

from amtdan.datasets import TaskSpec


class SeverityLabelNamesTest(unittest.TestCase):
    def test_invalid_or_visually_duplicate_labels_are_rejected(self):
        for label in (" ", None, 7, " mild "):
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, "non-empty ordered severity labels"):
                    TaskSpec("task", ("none", "mild", "moderate", "marked", label))

    def test_distinct_labels_keep_declared_order(self):
        labels = ("none", "mild", "moderate", "marked", "severe")
        self.assertEqual(TaskSpec("task", labels).severity_labels, labels)
