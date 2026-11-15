from decimal import Decimal
import unittest

from amtdan.datasets import ModalityState
from amtdan.models import GateWeights, compute_gate


class GateNumericInputsTest(unittest.TestCase):
    def test_decimal_quality_and_logits_can_be_mixed_with_floats(self):
        state = ModalityState(True, True, Decimal("0.25"))
        self.assertEqual(compute_gate(state, visual_logit=Decimal("0"), clinical_logit=0.0),
                         GateWeights(0.2, 0.8))

    def test_large_logit_difference_stays_finite(self):
        state = ModalityState(True, True, 0.5)
        self.assertEqual(compute_gate(state, visual_logit=-60000.0, clinical_logit=60000.0),
                         GateWeights(0.0, 1.0))
