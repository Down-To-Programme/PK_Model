from scipy import signal
import numpy as np


class Protocol:
    """A Pharmokinetic (PK) protocol

    This class protocol sets up the dosing protocol for a pharmokinetic model.
    This includes setting the amount of dose X ng either continous, multiple,
    or single application. Furthermore sets up the dosing type between
    subcutaneous and intravenous.

    Parameters
    ----------
    dose_amount: numeric, optional, default=1
        This parameter takes in the amount of dose given - X ng

    subcutaneous: logical, optional, default = False
        This parameter is set to False for intavenous dosing and True for
        subcutaneous dosing.

    k_a: numerical, optional, dafault = 1
        This parameter specifies the absorption rate for the subcutaneous
        dosing.

    continuous: logical, optional, default = False
        This parameter specifies whether or not the dose X ng is applied at
        a continuous rate of X ng per hour.

    continuous_period: numerical list, optional, default = [0, 0]
        This parameter specifies the time period over which continuous
        dosing is applied. The first number in the list is the time at which
        continuous dosing begins and the second number is when continuous
        dosing ends.

    instantaneous: logical, optional, default = True
        This parameter specifies whether any instantaneous doses of X ng
        take place.

    dose_times: numerical list, optional, default = [0]
        This parameter is a list of numerics that specify the times at which
        instantaneous doses of X ng are applied.

    Methods
    -------
    The method dose_time_function() for a particular time ouputs the dose(t).

    Several other methods have been defined to allow modifcation of the dosing
    protocol without the necessity of reinitialising the protocol for every
    modification. These are listed below:

    change_dose(), make_subcutaneous(), make_continuous(), add_dose_time()

    """
    def __init__(self, dose_amount=1, subcutaneous=False,
                 k_a=1, continuous=False, continuous_period=[0, 0],
                 instantaneous=True, dose_times=[0]):
        self.subcutaneous = subcutaneous
        self.k_a = k_a
        self.dose_amount = dose_amount
        self.continuous = continuous
        self.instantaneous = instantaneous
        self.continuous_period = continuous_period
        self.dose_times = dose_times
        self.dose_times.sort()

    def change_dose(self, dose_amount):
        """

        Paramater: dose_amount: The dosage given - X ng


        This method modfies the dose_amount parameter in the object of protocol
        class it is called on.

        """
        self.dose_amount = dose_amount

    def make_subcutaneous(self, k_a):
        """

        Paramater: k_a: the absorption rate for the subcutaneous dosing.


        This method modfies an object of class Protocol to change to
        subcutaneous dosing and specifies the k_a values for that dosing type.

        """
        self.k_a = k_a
        self.subcutaneous = True

    def make_continuous(self, time_added, time_removed):
        """

        Paramater: time_added: The time that at which want continuous dosing to
        start.
        Parameter: time_removed: The time at whcih you want continuosu dosing
        to end.


        This method modifies an object of class Protocol to convert the dosing
        protocol to continuous over a user specified time period.

        """
        self.continuous = True
        self.continuous_period[0] = time_added
        self.continuous_period[1] = time_removed

    def add_dose_time(self, time):
        """

        Paramater: time: Additional time at which you want there to be an
        instantaneous dose of X ng.


        This method modifies an object of class Protocol to add an additional
        user specified instantaneous dose time.

        """
        self.dose_times.append(time)
        self.dose_times.sort()

    def dose_time_function(self, t):
        """

        Paramater: t: time at which you want dose(t) to be returned.


        Returns: Dose(t) for the specific dosing protocol set up in the object
        of class Protocol.

        """
        dose_t_continuous, dose_t_instant = 0, 0
        if self.instantaneous:
            if t in self.dose_times:
                dose_t_instant = self.dose_amount


        # My attempt at implementing the gaussian shit 
        # I have a feeling this is not a good way to do this 
        # I'm not sure what you guys think David, Matthew? 
        # I will need to update testing for this at some point 
        gaussian = signal.gaussian(50, 0.5)
        if self.instantaneous:
            for item in self.dose_times:
                if t < item + 0.01 and t > item - 0.01:
                    times = np.linspace(start=item - 0.01, stop=item + 0.01,
                                        num=50)
                    times = list(times)
                    if t in times:
                        index = times.index(t)
                        dose_t_instant = gaussian[index] * self.dose_amount

        if self.continuous:
            if t < self.continuous_period[1] and \
               t >= self.continuous_period[0]:
                dose_t_continuous = self.dose_amount

        dose_t = dose_t_continuous + dose_t_instant
        return dose_t





