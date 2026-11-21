import unittest

from amtdan.datasets import ModalityState


class AvailabilityTypesTest(unittest.TestCase):
    def test_text_and_numeric_flags_cannot_enable_missing_modalities(self):
        for visual, clinical in (("false", False), (False, "false"), (1, False), (False, 0), ([], True)):
            with self.subTest(visual=visual, clinical=clinical):
                with self.assertRaisesRegex(ValueError, "boolean"):
                    ModalityState(visual, clinical)

    def test_boolean_availability_preserves_supported_combinations(self):
        for visual, clinical in ((True, False), (False, True), (True, True)):
            state = ModalityState(visual, clinical)
            self.assertIs(state.visual_available, visual)
            self.assertIs(state.clinical_available, clinical)
