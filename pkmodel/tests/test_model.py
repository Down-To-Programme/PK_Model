import unittest
import pkmodel as pk


class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        model = pk.Model(Vc=2., Vps=[], Qps=[], CL=3.)
        self.assertIsInstance(model, pk.Model)
        self.assertIsInstance(model.Vps, list)
        self.assertIsInstance(model.Qps, list)
        self.assertIsInstance(model.CL, float)
        self.assertEqual(model.size, 1)

    def test_add_compartment(self):
        """
        Tests add_compartment function
        """
        model = pk.Model(Vc=2, Vps=[], Qps=[], CL=3)
        model.add_compartment()
        self.assertEqual(model.size, 2)

    def test_properties(self):
        """
        Tests Vc, Vps, Qps, and CL properties
        """
        model = pk.Model(Vc=2., Vps=[], Qps=[], CL=3.)
        model.add_compartment()
        self.assertEqual(len(model.Vps), model.size - 1)
        self.assertEqual(len(model.Qps), model.size - 1)
        self.assertIsInstance(model.Vc, float)
        self.assertIsInstance(model.CL, float)




