import unittest
import pkmodel as pk


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
                             instantaneous=True, dose_times=[0, 1, 2, 3])
        dose_0 = dosing.dose_time_function(0)
        dose_1 = dosing.dose_time_function(1)
        dose_2 = dosing.dose_time_function(2)
        dose_3 = dosing.dose_time_function(3)
        dose_4 = dosing.dose_time_function(4)

        self.assertEqual(dose_0, 10)
        self.assertEqual(dose_1, 20)
        self.assertEqual(dose_2, 10)
        self.assertEqual(dose_3, 10)
        self.assertEqual(dose_4, 0)
