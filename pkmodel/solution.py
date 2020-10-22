#
# Solution class
#

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate


class Solution:
    """A Pharmokinetic (PK) model solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    model: using model class

    """
    def __init__(self, model, dose, tmax=1, nsteps=1000):
        self.model = model
        self.y0 = np.zeros(self.model.size)  # only central compartment n=1
        # one periphal comartment n=2, two periphal compartment n=3
        self.sol = np.zeros(self.model.size)
        self.t_eval = np.linspace(0, tmax, nsteps)
        self.dose = dose

    def rhs(self, t, y):  # so far only intravenous
        state = y
        # transitions = []
        V_c = self.model.Vc

        CL = self.model.CL
        cleared = state[0] / V_c * CL
        dq_dt = [0]
        flux_sum = 0
        # loop over peripheral compartments
        for comp in range(1, self.model.size):
            Q_pi = self.model.Qps[comp - 1]
            V_pi = self.model.Vps[comp - 1]
            flux = Q_pi * (state[0] / V_c - state[comp] / V_pi)
            dq_dt.append(flux)
            flux_sum += flux
        dq_dt[0] = self.dose(t) - cleared - flux_sum
        return dq_dt

    def solver(self):
        # args = []
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self.rhs(t, y),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval
        )
        self.sol = sol
        return sol

    def generate_plot(self):
        """
        Generate a plot of the drug quantity per
        compartment over time for the corresponding model
        
        returns: matplotlib figure
        """
        sol = self.solver()
        fig = plt.figure()
        plt.plot(sol.t, sol.y[0, :], label='- q_c')
        # loop over peripheral compartments and plot drug quantity for each
        for i in range(self.model.size - 1):
            label = '- q_p' + str(i + 2)
            plt.plot(sol.t, sol.y[i + 1, :], label=label)
        # show legend and axes labels
        plt.legend()
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
        plt.show()
        return fig

