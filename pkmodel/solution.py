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
    def __init__(self, model, protocol, tmax=1, nsteps=1000):
        self.model = model
        self.protocol = protocol
        self.t_eval = np.linspace(0, tmax, nsteps)
        self.solver()

    def rhs(self, t, y):  # intravenous
        state = y
        Vc = self.model.Vc
        CL = self.model.CL
        cleared = state[0] / Vc * CL
        dq_dt = [0]  # [dqc, dq_p1, dq_p2]

        flux_sum = 0
        # loop over peripheral compartments
        for comp in range(1, self.model.size):
            Q_pi = self.model.Qps[comp - 1]
            V_pi = self.model.Vps[comp - 1]
            flux = Q_pi * (state[0] / Vc - state[comp] / V_pi)
            dq_dt.append(flux)
            flux_sum += flux
        dq_dt[0] = self.protocol.dose_time_function(t) - cleared - flux_sum
        return dq_dt

    def rhs_sub(self, t, y):  # subsutaneous
        state = y   # one dim more than intravenous
        Vc = self.model.Vc
        CL = self.model.CL
        cleared = state[1] / Vc * CL
        dq_dt = [0, 0]  # [dq0, dqc, dq_p1, dq_p2]
        dq0_dt = self.protocol.dose_time_function(t)
        - self.protocol.k_a * state[0]
        dq_dt[0] = dq0_dt
        flux_sum = 0
        # loop over peripheral compartments
        for comp in range(1, self.model.size):
            Q_pi = self.model.Qps[comp - 1]
            V_pi = self.model.Vps[comp - 1]
            flux = Q_pi * (state[1] / Vc - state[comp + 1] / V_pi)
            dq_dt.append(flux)
            flux_sum += flux
        dq_dt[1] = self.protocol.k_a * state[0] - cleared - flux_sum
        return dq_dt

    def solver(self):
        if self.protocol.subcutaneous:
            step_func = self.rhs_sub
            self.y0 = np.zeros(self.model.size + 1)
            self.sol = np.zeros(self.model.size + 1)
        else:
            step_func = self.rhs
            # only central compartment n=1, one periphal comartment n=2
            # two periphal compartment n=3
            self.y0 = np.zeros(self.model.size)
            self.sol = np.zeros(self.model.size)

        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: step_func(t, y),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval
        )
        self.sol = sol
        return sol

