import matplotlib.pylab as plt
import pathlib


def make_model():
    from pkmodel import model
    from pkmodel import protocol
    from pkmodel import solution
    Vc, Vps, Qps, CL = input_model()
    model = model.Model(Vc=Vc, Vps=Vps, Qps=Qps, CL=CL)
    dose, sub, k_a, cont, cont_period, inst, dose_times = input_protocol()
    protocol = protocol.Protocol(dose, sub, k_a, cont, cont_period,
                                 inst, dose_times)
    sol = solution.Solution(model, protocol)
    return sol


def input_model():
    print('\nEnter volume of central compartment:')
    Vc = float(input("Vc (mL) = "))
    print('\nEnter number of peripheral compartments:')
    n = int(input("n = "))
    Vps = []
    Qps = []
    for i in range(n):
        print('\nEnter volume of peripheral compartment %d:' % (i + 1))
        Vp = input("Vp (mL) = ")
        Vps.append(float(Vp))
        print('\nEnter transition rate between central and '
              'peripheral compartment %d:' % (i + 1))
        Qp = input("Qp (mL/h) = ")
        Qps.append(float(Qp))
    print('\nEnter clearance rate from central compartment:')
    CL = float(input("CL (mL/h) = "))
    return Vc, Vps, Qps, CL


def input_k_a():
    print('\nDosing protocol can be either subcutaneous (s) '
          'OR intravenous bolus (i) ')
    protocol = str(input('Enter dosing protocol: (s/i) [i] ') or 'i')
    if (protocol != 's' and protocol != 'i'):
        print('Could not interpret protocol. '
              'Running with default (intravenous)')
    sub = False
    k_a = 1
    if protocol == 's':
        sub = True
        print('\nEnter absorption rate of drug '
              'administration for subcutaneous dosing:')
        k_a = input('k_a (/h): [1] ') or 1
        try:
            k_a = float(k_a)
        except ValueError:
            print('Could not interpret k_a. Running with default (1 /h)')
            k_a = 1
    return sub, k_a


def input_inst():
    print('\nEnter the number of instantaneous doses '
          'of X ng (default=1): ')
    n_inst = input('n = ') or 1
    dose_times = []
    inst = True
    try:
        n_inst = int(n_inst)
    except ValueError:
        print('Could not interpret n. Running with default (1)')
        n_inst = 1
    if n_inst < 1:
        inst = False
        n_inst = 0
    else:
        d0 = input('Time (in hours) of first dose: [0] ') or 0
        try:
            d0 = float(d0)
        except ValueError:
            print('Could not interpret time. Running with default (0)')
            d0 = 0
        dose_times.append(d0)
        for i in range(n_inst - 1):
            d = input('Time (in hours) of dose %d: ' % (i + 2))
            try:
                d = float(d)
                dose_times.append(d)
            except ValueError:
                print('Could not interpret time. Running with default (None)')
    return inst, dose_times


def input_cont():
    print('\nEnter whether the dose is applied '
          'at a continuous rate of X ng per hour: ')
    cont = str(input('Continuous?: (y/n) [n] ') or 'n')
    if (cont != 'y' and cont != 'n'):
        print('Could not interpret protocol. '
              'Running with default (not continuous)')
    continuous = False
    cont_period = [0, 0]
    if cont == 'y':
        continuous = True
        print('Enter time in hours at which continuous '
              'dosing begins (default=0):')
        t0 = float(input('t0 = ') or 0)
        print('Enter time in hours at which continuous '
              'dosing ends (default=0):')
        tf = float(input('tf = ') or 0)
        cont_period = [t0, tf]
    return continuous, cont_period


def input_protocol():
    print('\nEnter protocol of drug administration:')
    dose = float(input('Enter the dose amount in ng: [1] ') or 1.)
    try:
        dose = float(dose)
    except ValueError:
        print('Could not dose amount. Running with default (1 ng)')
        dose = 1

    sub, k_a = input_k_a()
    continuous, cont_period = input_cont()
    inst, dose_times = input_inst()

    return dose, sub, k_a, continuous, cont_period, inst, dose_times


def ask_show():
    show = str(input('\nShow the plot in pop-up window? (y/n) [y] \n') or 'y')
    if show != 'n' and show != 'y':
        print('Could not interpret input. Running with default (y)')
        return True
    if show == 'y':
        return True
    elif show == 'n':
        return False


def ask_save():
    save = str(input('\nSave the figure? (y/n) [n] \n') or 'n')
    if save != 'n' and save != 'y':
        print('Could not interpret input. Running with default (n)')
        return False
    if save == 'n':
        return False
    elif save == 'y':
        default_path = str(pathlib.Path(__file__).parent.absolute()) + '/'
        filename = input('Enter filename for figure [\'pkplot.pdf\']: ')
        path = input('Enter path for figure [%s]: ' % default_path)
        if path:
            filepath = '' + path + filename
        else:
            filepath = '' + default_path + filename
        print('Saving image at %s.pdf' % filepath)
        return filepath


def print_intro():
    print('\n=====================================')
    print('PK MODEL: SIMULATING PHARMACOKINETICS')
    print('=====================================\n \n')
    print('This is a package to run a user-specifed pharmacokinetic '
          'model (PK model).')
    print('The user can specify the number of peripheral compartments '
          'around a central compartment,')
    print('a dosing type (I.V. or S.C.), and a dosing protocol. '
          'A solver will solve the differential')
    print('equations that model the pharmacokinetics of the compartments, '
          'and graphs comparing the')
    print('solutions of different model parameters will be outputted.')
    print('Default values are within brackets (e.g. [0]).\n \n')

    print('Enter the parameters of the main model and protocol:')
    print('___________________________________________________')


if __name__ == "__main__":
    print_intro()
    solution1 = make_model()

    print(' \n================ \nPreparing plots. \n================')
    separate = input('\nSeparate the plots by compartment? (y/n) [n] ') or 'n'
    compare = input('\nCompare the plot with another model? (y/n) [n] ') or 'n'
    if compare == 'y':
        print('\nEnter the parameters of the second model and protocol.')
        print('_____________________________________________________')
        solution2 = make_model()
        if separate == 'y':
            fig = solution1.generate_plot(solution2, True, False, ask_save())
        else:
            fig = solution1.generate_plot(solution2, False, False, ask_save())
    elif separate == 'y':
        fig = solution1.generate_plot(None, True, False, ask_save())
    else:
        fig = solution1.generate_plot(None, False, False, ask_save())
    if ask_show():
        plt.show()
