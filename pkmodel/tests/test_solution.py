import unittest
from unittest.mock import Mock
import pkmodel as pk
import numpy as np
import matplotlib


class SolutionTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    Init calls solver and so the output of solver is also tested.
    """
    def test_intravenous(self):
        """
        Tests Solution creation for intravenous protocol.
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

    def test_subcutaneous(self):
        """
        Tests Solution creation for subcataneous protocol.
        """
        mock_model = Mock()
        mock_model.size = 2
        mock_model.Vc = 1
        mock_model.CL = 1
        mock_model.Qps = [1]
        mock_model.Vps = [1]
        mock_protocol = Mock()
        mock_protocol.subcutaneous = True
        mock_protocol.k_a = 1
        mock_protocol.dose_time_function.return_value = 1

        solution = pk.Solution(model=mock_model, protocol=mock_protocol)
        self.assertEqual(solution.sol.y.shape[0], solution.model.size + 1)
        self.assertEqual(solution.sol.y.shape[1], solution.t_eval.shape[0])
        self.assertIsInstance(solution.t_eval, np.ndarray)
        self.assertIsInstance(solution.y0, np.ndarray)

    def test_plotting(self):
        """
        Tests Solution for the ability to create separate plots for solutions.
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

        sol_fig = solution.generate_plot()
        self.assertIsInstance(sol_fig, matplotlib.figure.Figure)

    def test_plotting_separate(self):
        """
        Tests Solution for the ability to create separate plots for solutions.
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

        sol_fig = solution.generate_plot(separate=True)
        self.assertIsInstance(sol_fig, matplotlib.figure.Figure)

