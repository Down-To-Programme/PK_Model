import matplotlib.pylab as plt
import numpy as np
import scipy.integrate

from pkmodel import model
from pkmodel import solution
from pkmodel import protocol

protocol1 = protocol.Protocol(dose_amount=1, subcutaneous=False,
                 k_a=1, continuous=True, continuous_period=[0, 1],
                 instantaneous=False, dose_times=[0])
print(protocol1.dose_time_function(0))
print(protocol1.k_a)

protocol2 = protocol.Protocol(dose_amount=1, subcutaneous=True,
                 k_a=1, continuous=True, continuous_period=[0, 1],
                 instantaneous=False, dose_times=[0])

model1 = model.Model(Vc=1., Vps=[1.,1.], Qps = [1.,2.], CL=3.)

print('Model size ', model1.size)
print('Volume of central compartment ', model1.Vc)
print('Compartment volumes', model1.Vps)
print('Transition rates', model1.Qps)
print('Clearance rate', model1.CL)

solution1 = solution.Solution(model1, protocol1)
solution2 = solution.Solution(model1, protocol2)
solution1.generate_plot(compare=solution2,
                      separate=False, show=True, savefig=True)
