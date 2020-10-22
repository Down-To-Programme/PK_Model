import unittest
from unittest.mock import Mock
import pkmodel as pk
import numpy as np


class SolutionTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    Init calls solver and so the output of solver is also tested.
    """
    def test_create(self):
        """
        Tests Solution creation.

        needs to take protocol
        protocol.subcutaneous = false
        protocol.dose_time_function(t) = 1


        needs to take model
        model.size=2
        model.Vc = 1
        model.CL = 1
        model.Qps[comp - 1] = [1]
        model.Vps[comp - 1] = [1]


        """
        mock_model = Mock()
        mock_model.size = 2
        mock_model.Vc = 1
        mock_model.CL = 1
        mock_model.Qps = [1]
        mock_model.Vps = [1]
        mock_protocol = Mock()
        mock_protocol.subcutaneous = False
        mock_protocol.dose_time_function.return_value = 1

        solution = pk.Solution(model=mock_model, protocol=mock_protocol)
        self.assertEqual(solution.sol.y.shape[0], solution.model.size)
        self.assertEqual(solution.sol.y.shape[1], solution.t_eval.shape[0])
        self.assertIsInstance(solution.t_eval, np.ndarray)
        self.assertIsInstance(solution.y0, np.ndarray)

    # def test_rhs(self):
    #     """
    #     Tests rhs function.
    #     """
    #     model = pk.Model(Vc=2, Vps=[], Qps=[], CL=3)
    #     mock_dose = Mock(name="dose", return_value=0)
    #     solution = pk.Solution(model=model, dose=mock_dose)
    #     self.assertIsNotNone(solution.rhs(0, [0, 0]))

    # def test_solver(self):
    #     """
    #     Tests solver function.
    #     """
    #     model = pk.Model(Vc=2, Vps=[], Qps=[], CL=3)
    #     mock_dose = Mock(name="dose", return_value=0)
    #     solution = pk.Solution(model=model, dose=mock_dose)
    #     self.assertIsNotNone(solution.solver())



