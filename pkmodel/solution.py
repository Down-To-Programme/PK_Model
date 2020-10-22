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

    def generate_plot(self, separate=False):
        """
        Generate a plot of the drug quantity per
        compartment over time for the corresponding model

        :param separate: set to True if you want 1 plot per compartment
        :returns: matplotlib figure
        """
        sol = self.solver()
        n = self.model.size
        if separate:
            fig = plt.figure(figsize=(n * 4.0, 3.0))
            central = fig.add_subplot(1, n, 1)
            central.plot(sol.t, sol.y[0, :], label='- q_c')
            central.legend()
            central.set_title('Central compartment')
        else:
            fig = plt.figure()
            plt.plot(sol.t, sol.y[0, :], label='- q_c')

        # add legend and axes labels
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')

        # loop over peripheral compartments and plot drug quantity for each
        for i in range(n - 1):
            label = '- q_p' + str(i + 2)
            if separate:
                subplot = fig.add_subplot(1, n, i + 2)
                subplot.plot(sol.t, sol.y[i + 1, :], label=label)
                subplot.legend()
                subplot.set_xlabel('time [h]')
                subplot.set_title('Peripheral compartment #' + str(i + 1))
            else:
                plt.plot(sol.t, sol.y[i + 1, :], label=label)
        plt.legend()
        fig.tight_layout()
        plt.show()
        return fig
