from decimal import Decimal
import unittest

from amtdan.models import GateWeights, fuse_embeddings


class FusionNumericTypesTest(unittest.TestCase):
    def test_decimal_weights_and_embeddings_use_the_same_arithmetic(self):
        weights = GateWeights(Decimal("0.25"), Decimal("0.75"))
        result = fuse_embeddings([Decimal("2"), Decimal("4")], [Decimal("6"), Decimal("8")], weights)
        self.assertEqual(result, (5.0, 7.0))
        self.assertIs(type(weights.visual), float)
        self.assertTrue(all(type(value) is float for value in result))

    def test_decimal_embedding_works_with_a_single_available_modality(self):
        self.assertEqual(fuse_embeddings(None, [Decimal("3")], GateWeights(0, 1)), (3.0,))
