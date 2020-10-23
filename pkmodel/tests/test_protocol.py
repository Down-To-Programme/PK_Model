import unittest
import pkmodel as pk
import numpy as np


class ProtocolTest(unittest.TestCase):
    """
    Tests the :class:`Protocol` class.
    """
    def test_create(self):
        """
        Tests Protocol creation.
        """
        dosing = pk.Protocol(dose_amount=10, subcutaneous=True,
                             k_a=0.3, continuous=True,
                             continuous_period=[1, 2],
                             instantaneous=True, dose_times=[0, 1, 2, 3])

        self.assertEqual(dosing.dose_amount, 10)
        self.assertEqual(dosing.subcutaneous, True)
        self.assertEqual(dosing.k_a, 0.3)
        self.assertEqual(dosing.continuous, True)
        self.assertEqual(dosing.continuous_period, [1, 2])
        self.assertEqual(dosing.instantaneous, True)
        self.assertEqual(dosing.dose_times, [0, 1, 2, 3])

    def test_dose_function(self):
        dosing = pk.Protocol(dose_amount=10, subcutaneous=True,
                             k_a=0.3, continuous=True,
                             continuous_period=[1, 2],
                             instantaneous=False)
        dose_0 = dosing.dose_time_function(0)
        dose_1 = dosing.dose_time_function(0.5)
        dose_2 = dosing.dose_time_function(1.1)
        dose_3 = dosing.dose_time_function(1.8)
        dose_4 = dosing.dose_time_function(4)

        self.assertEqual(dose_0, 0)
        self.assertEqual(dose_1, 0)
        self.assertEqual(dose_2, 10)
        self.assertEqual(dose_3, 10)
        self.assertEqual(dose_4, 0)

    def test_both_dose(self):
        dosing = pk.Protocol(dose_amount=10, subcutaneous=True,
                             k_a=0.3, continuous=True,
                             continuous_period=[1, 2],
                             instantaneous=True, instant_doses=[10, 20],
                             dose_times=[0.5, 1.5])

        dose_0 = dosing.dose_time_function(0.5)
        dose_1 = dosing.dose_time_function(1.5)

        self.assertLessEqual(dose_0 - (10 / (0.02 * np.sqrt(2 * np.pi))),
                             0.0001)
        self.assertLessEqual(dose_1 - (10 + 20 / (0.02 * np.sqrt(2 * np.pi))),
                             0.0001)

    def test_change_dose(self):
        dosing = pk.Protocol()

        self.assertEqual(dosing.dose_amount, 1)
        dosing.change_dose(100)
        self.assertEqual(dosing.dose_amount, 100)

    def test_modify_dose_type(self):
        dosing = pk.Protocol()
        self.assertEqual(dosing.subcutaneous, False)
        dosing.modify_dose_type(True, 0.3)
        self.assertEqual(dosing.subcutaneous, True)
        self.assertEqual(dosing.k_a, 0.3)

    def test_make_continuous(self):
        dosing = pk.Protocol()
        self.assertEqual(dosing.continuous, False)
        self.assertEqual(dosing.continuous_period, [0, 0])
        dosing.make_continuous(4, 10)
        self.assertEqual(dosing.continuous, True)
        self.assertEqual(dosing.continuous_period, [4, 10])

    def test_add_dose(self):
        dosing = pk.Protocol(instantaneous=False, instant_doses=[],
                             dose_times=[])
        self.assertEqual(dosing.instantaneous, False)
        self.assertEqual(dosing.dose_times, [])
        self.assertEqual(dosing.instant_doses, [])

        dosing.add_dose(1, 1)
        self.assertEqual(dosing.instantaneous, True)
        self.assertEqual(dosing.dose_times, [1])
        self.assertEqual(dosing.instant_doses, [1])

        dosing.add_dose(5, 1)
        self.assertEqual(dosing.instantaneous, True)
        self.assertEqual(dosing.dose_times, [1, 5])
        self.assertEqual(dosing.instant_doses, [1, 1])
