import unittest
from unittest.mock import Mock
import pkmodel as pk
import numpy as np


class SolutionTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    """
    def test_create(self):
        """
        Tests Solution creation.
        """
        model = pk.Model(Vc=2, Vps=[], Qps=[], CL=3)
        mock_dose = Mock(name="dose", return_value=0)
        solution = pk.Solution(model=model, dose=mock_dose)
        self.assertIsInstance(solution.sol, np.ndarray)
        self.assertIsInstance(solution.t_eval, np.ndarray)
        self.assertIsInstance(solution.y0, np.ndarray)

    def test_rhs(self):
        """
        Tests rhs function.
        """
        model = pk.Model(Vc=2, Vps=[], Qps=[], CL=3)
        mock_dose = Mock(name="dose", return_value=0)
        solution = pk.Solution(model=model, dose=mock_dose)
        self.assertIsNotNone(solution.rhs(0, [0, 0]))

    def test_solver(self):
        """
        Tests solver function.
        """
        model = pk.Model(Vc=2, Vps=[], Qps=[], CL=3)
        mock_dose = Mock(name="dose", return_value=0)
        solution = pk.Solution(model=model, dose=mock_dose)
        self.assertIsNotNone(solution.solver())



