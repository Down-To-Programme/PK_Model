import matplotlib.pylab as plt
import numpy as np
import scipy.integrate

from pkmodel import model
from pkmodel import solution
import test_protocol

# def dose(t, X=1):
#     return X

protocol = test_protocol.Protocol(dose_amount =1., subcutaneous=True, 
    k_a=100, continuous=True, continuous_period=[0, 0], dose_times=[],
    multiple=False)
print(protocol.dose_time_function(0))
print(protocol.k_a)

model1 = model.Model(Vc=1., Vps=[1.,1.], Qps = [100.,2.], CL=3.)

print('Model size ', model1.size)
print('Volume of central compartment ', model1.Vc)
print('Compartment volumes', model1.Vps)
print('Transition rates', model1.Qps)
print('Clearance rate', model1.CL)

solution1 = solution.Solution(model1, protocol)
sol = solution1.solver()
#print(sol)

fig = plt.figure()
plt.plot(sol.t, sol.y[0, :], label='- q_0')
plt.plot(sol.t, sol.y[1, :], label='- q_c')
plt.plot(sol.t, sol.y[2, :], label='- q_p1')
plt.plot(sol.t, sol.y[3, :], label='- q_p2')
plt.legend()
plt.ylabel('drug mass [ng]')
plt.xlabel('time [h]')
plt.show()