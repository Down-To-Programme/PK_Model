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

    instant_doses: numerical list, optional, default = [1].
        This parameter is a list of numerics that specify the doses of X ng
        given instantaneously at the times specified in the dose_times param.

    Methods
    -------
    The method dose_time_function() for a particular time ouputs the dose(t).

    Several other methods have been defined to allow certain modifcations of
    the dosing protocol without the necessity of reinitialising the protocol
    for every modification. Until other functions are supported other
    modifications require reintialising the object of class Protocol.
    Supported methods are listed below:

    change_dose(), modify_dose_type(), make_continuous(), add_dose()

    """
    def __init__(self, dose_amount=1, subcutaneous=False,
                 k_a=1, continuous=False, continuous_period=[0, 0],
                 instantaneous=True, dose_times=[0], instant_doses=[1]):
        self.subcutaneous = subcutaneous
        self.k_a = k_a
        self.dose_amount = dose_amount
        self.continuous = continuous
        self.instantaneous = instantaneous
        self.continuous_period = continuous_period
        self.dose_times = dose_times
        self.instant_doses = instant_doses

    def change_dose(self, dose_amount):
        """

        Paramater: dose_amount: The dosage given - X ng


        This method modfies the dose_amount parameter in the object of protocol
        class it is called on.

        """
        self.dose_amount = dose_amount

    def modify_dose_type(self, subcutaneous, k_a=1):
        """

        Paramater: subcutaneous: boolean, required.
            When set as True this specifies there is subcutaneous dosing, and
            when False it specifies intravenous dosing.
        Paramater: k_a: numeric, optional, default = 1.
            The absorption rate for the subcutaneous dosing.


        This method modfies an object of class Protocol to allow users to
        specifiy whether there is subcutaneous or intravenous dosing.
        Additionally for subcutaneous dosing it allows users to modify the
        value of k_a.

        """
        self.k_a = k_a
        if subcutaneous:
            self.subcutaneous = True
        else:
            self.subcutaneous = False

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

    def add_dose(self, time, dose):
        """

        Paramater: time: numeric, required
            Additional time at which you want there to be an instantaneous
            dose.
        Paramater: dose: numeric, required
            The dose in ng that you want applied at this timepoint.


        This method modifies an object of class Protocol to add an additional
        user specified instantaneous dose of dose ng at time. The method
        also specifies that instantaneous dosing does happen should it not
        already be specified.

        """
        self.dose_times.append(time)
        self.instant_doses.append(dose)
        self.instantaneous = True

    def dose_time_function(self, t):
        """

        Paramater: t: numeric, required.
            The time at which you want dose(t) to be returned.

        Returns: numeric.
            Dose(t) for the specific dosing protocol set up in the object
        of class Protocol.

        """
        dose_t_continuous, dose_t_instant = 0, 0
        dose_width = 0.02

        for dose_size, dose_time in zip(self.instant_doses,
                                        self.dose_times):
            dose_t_instant += easy_gaus(t, dose_time, dose_width) * dose_size \
                * self.instantaneous

        if self.continuous and t < self.continuous_period[1] and \
           t >= self.continuous_period[0]:
            dose_t_continuous = self.dose_amount

        dose_t = dose_t_continuous + dose_t_instant
        return dose_t


def easy_gaus(x, mean, std):
    """
    A function which returns generates a gausssian fucntion from user inputted
    mean and std deviation parameters and returns the value of the function at
    user inputted x.

    Parameter: x: numeric, required
        The value at which you wish the gaussian function to be evaluated.
    Parameter: mean: numeric, required
        The mean or the positon on the x axis at which the gaussian function
        is centred or at its peak.
    Parameter: std: numeric, required
        The standard deviation of the gaussian function.
    Returns: float
        The gaussian function evaluated at x, for the use specified parameters.


    """
    return np.exp(-0.5 * (((x - mean) / std)**2)) / (std * np.sqrt(2 * np.pi))



