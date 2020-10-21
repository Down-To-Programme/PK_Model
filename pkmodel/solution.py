#
# Solution class
#

import numpy as np
import scipy.integrate


class Solution:
    """A Pharmokinetic (PK) model solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    model: using model class

    """
    def __init__(self, model):
        self.model = model
        self.y0 = np.zeros(self.model.size)  # only central compartment n=1
        # one periphal comartment n=2, two periphal compartment n=3
        self.sol = np.zeros(self.model.size)
        self.t_eval = np.linspace(0, 1, 1000)

    def rhs(self, t, y):  # so far only intravenous
        state = y
        # transitions = []
        V_c = self.model.Vc
        CL = self.model.CL
        cleared = state[0] / V_c * CL
        dq_dt = [0]
        flux_sum = 0
        for comp in range(1, self.model.size):
            Q_pi = self.model.Qps[comp - 1]
            V_pi = self.model.Vps[comp - 1]
            flux = Q_pi * (state[0] / V_c - state[comp] / V_pi)
            dq_dt.append(flux)
            flux_sum += flux
        dq_dt[0] = dose(t, X) - cleared - flux_sum
        return dq_dt

    def solver(self):
        # args = []
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: rhs(t, y),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y, t_eval=self.t_eval
        )
        self.sol = sol
        return sol

