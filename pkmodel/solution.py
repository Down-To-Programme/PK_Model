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
    def __init__(self, model, dose, tmax=1, nsteps=1000): 
        ## dose -> protocol ; protocol.dose
        self.model = model
        self.t_eval = np.linspace(0, tmax, nsteps)
        self.dose = dose
        self.solver()

    def rhs(self, t, y): # so far only intravenous
        state = y
        transitions = []
        Vc = self.model.Vc
        CL = self.model.CL
        cleared = state[0] / Vc * CL
        dq_dt = [0]
        flux_sum = 0
        for comp in range(1, self.model.size): #loop over peripheral compartments
            Q_pi = self.model.Qps[comp-1]
            V_pi = self.model.Vps[comp-1]
            flux =  Q_pi * (state[0] / Vc - state[comp] / V_pi)
            dq_dt.append( flux )
            flux_sum += flux
        dq_dt[0] = self.dose(t) - cleared - flux_sum
        return dq_dt

    def solver(self):
        self.y0 = np.zeros(self.model.size)  # only central compartment n=1, one periphal comartment n=2, two periphal compartment n=3
        self.sol = np.zeros(self.model.size)
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self.rhs(t, y),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval
        )
        self.sol = sol
        return sol

