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

    def plot(self, separate=False):
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
            fig = plt.figure(figsize=(4.0, 3.0))
            model = fig.add_subplot(1, 1, 1)
            model.plot(sol.t, sol.y[0, :], label='- q_c')

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
                model.plot(sol.t, sol.y[i + 1, :], label=label)
        plt.legend()
        fig.tight_layout()
        plt.show()
        return fig

    def compare_plots(self, solution_2):
        """
        Generates a matplotlib figure with two subplots that show
        the drug quantity in each compartment over time for the models
        of self and solution_2

        :param solution_2: Should be a Solution object different from self

        :returns: Matplotlib Figure object
        """
        sol1 = self.solver()
        sol2 = solution_2.solver()
        n = max(self.model.size, solution_2.model.size)
        fig = plt.figure(figsize=(2 * 4.0, 3.0))
        model1 = fig.add_subplot(1, 2, 1)
        model1.set_title('Model 1')
        model1.set_xlabel('time [h]')
        model1.set_ylabel('drug mass [ng]')
        model2 = fig.add_subplot(1, 2, 2)
        model2.set_title('Model 2')
        model2.set_xlabel('time [h]')
        for i in range(n):
            if i == 0:
                label = '- q_c'
            else:
                label = '- q_p' + str(i + 1)
            if i < len(sol1.y):
                model1.plot(sol1.t, sol1.y[i, :], label=label)
            if i < len(sol2.y):
                model2.plot(sol2.t, sol2.y[i, :], label=label)
        model1.legend()
        model2.legend()
        fig.tight_layout()
        plt.show()

    def compare_separate(self, solution_2):
        """
        Generates a matplotlib figure that shows the drug quantity over time
        for the models self and solution_2, with one plot per compartment

        :param solution_2: Should be a Solution object different from self

        :returns: Matplotlib Figure object
        """
        sol1 = self.solver()
        sol2 = solution_2.solver()
        n = max(self.model.size, solution_2.model.size)
        fig = plt.figure(figsize=(n * 4.0, 3.0))
        central = fig.add_subplot(1, n, 1)
        central.plot(sol1.t, sol1.y[0, :], label='model 1')
        central.plot(sol2.t, sol2.y[0, :], label='model 2')
        central.legend()
        central.set_xlabel('time [h]')
        central.set_ylabel('drug mass [ng]')
        central.set_title('Central compartment')
        for i in range(n - 1):
            compartment = fig.add_subplot(1, n, i + 2)
            if i + 1 < len(sol1.y):
                compartment.plot(sol1.t, sol1.y[i + 1, :], label='model 1')
            if i + 1 < len(sol2.y):
                compartment.plot(sol2.t, sol2.y[i + 1, :], label='model 2')
            compartment.legend()
            compartment.set_xlabel('time [h]')
            compartment.set_title('Peripheral compartment #' + str(i + 1))
        fig.tight_layout()
        plt.show()
        return fig

    def generate_plot(self, compare=None, separate=False):
        """
        Calls appropriate function to generate plots of the drug
        quantity per compartment over time for the corresponding model

        :param compare: If None (default), function will only generate plot
        for the Solution object. If set to a Solution object, function will
        generate plots to compare the two models. Else, function will raise an
        Assertion Error.

        :param separate: If False (default), will show all compartments on the
        same plot. Set to True if you want 1 plot per compartment.
        """
        if compare is None:
            self.plot(separate=separate)
        else:
            assert type(compare) is Solution, 'compare should be a Solution'
            if not separate:
                self.compare_plots(compare)
            elif separate:
                self.compare_separate(compare)
        return
