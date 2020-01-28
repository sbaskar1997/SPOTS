#!/usr/bin/env python

# Optimal Control single shooting method for descent problem
# Author: Sandeep Baskar
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from descent_EOMS import *

'''
Generalize for any centerbody
Generalize for any scalar thrust and vehicle parameters
Tidy up graphics

'''

def shooting_method(initial_conditions, final_conditions):
    # Unpack intial conditions (including guesses for co-states)
    [x0, y0, vx_0, vy_0, l1_0, l2_0, l3_0, l4_0] = initial_conditions

    # Unpack final conditions
    [vx_f, vy_f, H_f, y_f] = final_conditions

    # Shooting method to iterate on constraints that arise from CoV
    def zerofun(x):
        [t_f, l2_0_g, l3_0_g, l4_0_g] = x
        ic = [x0, y0, vx_0, vy_0, l1_0, l2_0_g, l3_0_g, l4_0_g]
        if t_f == t_f:
            t = np.linspace(0,t_f,1000)
            sol = odeint(EOM_descent, ic, t)
            x = sol[:,0]
            y = sol[:,1]
            vx = sol[:,2]
            vy = sol[:,3]
            l1 = sol[:,4]
            l2 = sol[:,5]
            l3 = sol[:,6]
            l4 = sol[:,7]
            y_f_g = sol[:,1][-1]
            F = 1000
            m = 10000
            k1 = 1.225 * 1 * np.pi * 9/(2 * m)
            g = 3.986e14/((y[-1])**2)
            H_f_g = l1[-1] * vx[-1] + l2[-1] * vy[-1] - F/m * np.sqrt(l3[-1]**2 + l4[-1]**2) + k1 * np.exp(-y[-1]/100000) * ((l4[-1] * vy[-1] - l3[-1] * vx[-1])/np.sqrt(vx[-1]**2 + vy[-1]**2)) - l4[-1] * g
            return [H_f_g - H_f, vy_f - vy[-1], vx_f - vx[-1], y_f_g - y_f]
        else:
            return [10,10,10,10]

    # Have initial guesses to iterate on until constraints are satisfied
    gs = [30, l2_0, l3_0, l4_0]

    # Find the true initial conditions to solve the optimal control problem
    ic_act = opt.fsolve(zerofun, gs)

    # Set time to go from 0 (start) to final time at which problem is fully solved
    t = np.linspace(0,ic_act[0],1000)

    # Pack initial conditions
    ic_pack = [x0, y0, vx_0, vy_0, l1_0, ic_act[1], ic_act[2],ic_act[3]]

    # Solve EOMS and co-states
    sol = odeint(EOM_descent, ic_pack, t)

    # Unpack co-states necessary for control law formulation
    l4 = sol[:,7]
    l3 = sol[:,6]

    # Solve for control law
    t_th = np.divide(-l4,l3)

    # Plot trajectory and control law history
    plt.plot(sol[:,0],(sol[:,1] - 6378 * 1000))
    plt.show()
    plt.plot(t, t_th)
    plt.show()

if __name__ == '__main__':
    # Initial conditions
    x0 = 0
    y0 = 300 * 1000 + 6378 * 1000
    vx_0 = np.sqrt(398600/(1200 + 6378)) * 1000
    vy_0 = 0
    l1_0 = 0
    l2_0 = 1
    l3_0 = 1
    l4_0 = 1
    ic = [x0, y0, vx_0, vy_0, l1_0, l2_0, l3_0, l4_0]

    # Desired final cond
    vy_f = 0
    vx_f = np.sqrt(398600/(200 + 6378)) * 1000
    H_f = -1
    y_f = 1000*(6378 + 100)
    fc = [vx_f, vy_f, H_f, y_f]

    # Call shooting method function
    shooting_method(initial_conditions = ic, final_conditions = fc)
