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
        with model( Vc, Vps, Qps, CL)

    protocol: using protocoll class to specify
        intravenous or subcutaneous dosing
        dosing function needed

    tmax: float
        integrates until it reaches tmax
        default value is 1

    nsteps: int
        number of integration steps
        default value is 1000

    """
    def __init__(self, model, protocol, tmax=1, nsteps=1000):
        self.model = model
        self.protocol = protocol
        self.t_eval = np.linspace(0, tmax, nsteps)
        self.tmax = tmax
        self.nsteps = nsteps

        self.solver()

    def rhs_intravenous(self, t, y):
        '''
        Right hand side of flux equation for intravenous dosing protocol
        dimension of system = number of compartments = self.model.size
        only central compartment dim = 1
        one periphal comartment dim = 2
        two periphal compartment dim = 3
        Parameters
        ----------
        t: time
        y: state vector [qc, q_p1, q_p2]
        '''
        state = y
        Vc = self.model.Vc  # volume of the main compartment
        CL = self.model.CL  # Clearance rate

        cleared = state[0] / Vc * CL  # flux going out of the main compartment
        dq_dt = [0]  # [dqc, dq_p1, dq_p2]

        flux_sum = 0  # sum of flux between compartments
        # loop over peripheral compartments
        for comp in range(1, self.model.size):
            # transition rate etween main compartment
            # and i-th peripheral compartment
            Q_pi = self.model.Qps[comp - 1]
            # volume of i-th peripheral compartment
            V_pi = self.model.Vps[comp - 1]
            # flux between peripheral and main compartment
            flux = Q_pi * (state[0] / Vc - state[comp] / V_pi)
            dq_dt.append(flux)
            flux_sum += flux
        dq_dt[0] = self.protocol.dose_time_function(t) - cleared - flux_sum
        return dq_dt

    def rhs_subcutaneous(self, t, y):
        '''
        Right hand side of flux equation for subcutaneous dosing protocol
        dimension of system = number of compartments = self.model.size
        Parameters
        ----------
        t: time
        y: state vector [q0, qc, q_p1, q_p2]
        y has one dim more than in intravenous protocol
        q0 is an additional compartment from which the drug
        is absorbed to the central compartment
        '''
        state = y
        Vc = self.model.Vc  # volume of the main compartment
        CL = self.model.CL  # Clearance rate

        cleared = state[0] / Vc * CL  # flux going out of the main compartment
        dq_dt = np.zeros(self.model.size + 1)  # [dqc, dq_p1, dq_p2, dq0]
        dq0_dt = self.protocol.dose_time_function(t)
        dq0_dt -= self.protocol.k_a * state[-1]
        dq_dt[-1] = dq0_dt

        flux_sum = 0  # sum of flux between compartments
        # loop over peripheral compartments
        for comp in range(1, self.model.size):
            # transition rate etween main compartment
            # and i-th peripheral compartment
            Q_pi = self.model.Qps[comp - 1]
            # volume of i-th peripheral compartment
            V_pi = self.model.Vps[comp - 1]
            flux = Q_pi * (state[0] / Vc - state[comp] / V_pi)
            dq_dt[comp] = flux
            flux_sum += flux
        dq_dt[0] = self.protocol.k_a * state[-1] - cleared - flux_sum
        return dq_dt

    def solver(self):
        '''
        Runge-Kutta solver
        Dosing protocol specified in protocol class
        determines which rhs function will be used
        '''
        if self.protocol.subcutaneous:
            step_func = self.rhs_subcutaneous
            # subcutaneous protocol has one more dimension
            # than intravenous protocol
            # initial condition y0
            self.y0 = np.zeros(self.model.size + 1)
            self.sol = np.zeros(self.model.size + 1)
        else:
            step_func = self.rhs_intravenous
            # intial condition
            self.y0 = np.zeros(self.model.size)
            self.sol = np.zeros(self.model.size)

        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: step_func(t, y),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval,
            max_step=self.tmax / self.nsteps
        )
        self.sol = sol
        return sol

    def plot(self, separate=False):
        """
        Generate a figure of the drug quantity per
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

        # plot subcutanous injections compartment
        if self.protocol.subcutaneous and not separate:
            model.plot(sol.t, sol.y[-1, :], label='- q_0')

        plt.legend()
        fig.tight_layout()
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
        # plot subcutanous injections compartment
        if self.protocol.subcutaneous:
            model1.plot(sol1.t, sol1.y[-1, :], label='- q_0')
        if solution_2.protocol.subcutaneous:
            model2.plot(sol2.t, sol2.y[-1, :], label='- q_0')
        model1.legend()
        model2.legend()
        fig.tight_layout()
        return fig

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
        return fig

    def generate_plot(self, compare=None,
                      separate=False, show=False, savefig=False):
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
        fig = None
        if compare is None:
            fig = self.plot(separate=separate)
        else:
            assert type(compare) is Solution, 'compare should be a Solution'
            if not separate:
                fig = self.compare_plots(compare)
            elif separate:
                fig = self.compare_separate(compare)

        if show:
            plt.show()

        if type(savefig) is str:
            fig.savefig(savefig + '.pdf')
        elif savefig:
            fig.savefig('pkplot.pdf')

        return fig
