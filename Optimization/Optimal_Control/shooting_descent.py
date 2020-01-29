#!/usr/bin/env python

# Optimal Control single shooting method for descent problem
# Author: Sandeep Baskar

# Import native modules
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import sys, os

# Import custom modules
sys.path.insert(0, os.path.abspath('../..'))
from Optimization.Optimal_Control.descent_EOMS import *
from common.astro.solar_system import *

def shooting_method(initial_conditions, final_conditions, planet = None, Cd = 1.0, r_vehicle = 3, F = 1000, m = 10000):
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
            sol = odeint(EOM_descent, ic, t, args = (F, m))
            x = sol[:,0]
            y = sol[:,1]
            vx = sol[:,2]
            vy = sol[:,3]
            l1 = sol[:,4]
            l2 = sol[:,5]
            l3 = sol[:,6]
            l4 = sol[:,7]
            y_f_g = sol[:,1][-1]
            k1 = planet.rho_ref * Cd * np.pi * r_vehicle**2/(2 * m)
            g = planet.mu/((y[-1])**2)
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
    sol = odeint(EOM_descent, ic_pack, t, args = (F, m))

    # Unpack co-states necessary for control law formulation
    l4 = sol[:,7]
    l3 = sol[:,6]

    # Solve for control law
    t_th = np.divide(-l4,l3)

    # Plot trajectory
    plt.plot(sol[:,0]/1000,(sol[:,1] - planet.radius)/1000)
    plt.xlabel('Down/Cross-Range (km)')
    plt.ylabel('Altitude (km)')
    plt.title('Optimal Trajectory (Time minimization)')
    plt.grid('on')
    plt.show()

    # Plot control-law history
    plt.plot(t, t_th)
    plt.xlabel('time (s)')
    plt.ylabel('tan(\u03B8)')
    plt.title('Control Law History')
    plt.grid('on')
    plt.show()

if __name__ == '__main__':
    planet_m = mars(km = False)
    planet_km = mars(km = True)

    # Initial conditions & Initialization
    x0 = 0
    y0 = 600 * 1000 + planet_m.radius
    vx_0 = np.sqrt(planet_km.mu/(1500 + planet_km.radius)) * 1000
    vy_0 = 0
    l1_0 = 0
    l2_0 = 1
    l3_0 = 1
    l4_0 = 1
    ic = [x0, y0, vx_0, vy_0, l1_0, l2_0, l3_0, l4_0]


    # Desired final cond
    vy_f = 0
    vx_f = np.sqrt(planet_km.mu/(600 + planet_km.radius)) * 1000
    H_f = -1
    y_f = 1000 * (planet_km.radius + 100)
    fc = [vx_f, vy_f, H_f, y_f]

    # Call shooting method function
    shooting_method(initial_conditions = ic, final_conditions = fc, planet = planet_m)
