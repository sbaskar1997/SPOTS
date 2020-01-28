#!/usr/bin/env python

# Optimal Control EOMS for descent trajectory (2D analysis, flat planet)
# Author: Sandeep Baskar

'''TODO:
    Need to make code prettier
    Need to move cosd, sind to math helper
    Need to make code modular based off of atmosphere model
    Need to create trajectory class to hold data and control laws, etc.
    Need to update drag model
    Put main script execution as a different file
'''

# Import native modules
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import scipy.optimize as opt


def earth_atmo(alt):
    if alt > 25000:
        T = -131.21 + .00299 * alt
        p = 2.488 * ((T + 273.15)/216.6) ** -11.388
    elif (alt > 11000) and (alt <= 25000):
        T = -56.46
        p = 22.65 * np.exp(1.73 - .000157 * alt)
    else:
        T = 15.04 - .00649 * alt
        p = 101.29 * ((T + 273.1)/288.08)**5.256

    rho = p/(.2869 * (T + 273.15))
    p = p * 1000
    T = T + 273.15
    return [T, p, rho];

def cosd(arg):
    return np.cos(np.radians(arg))
def sind(arg):
    return np.sin(np.radians(arg))

def EOM_descent(states, t, Thrust = 1000, m = 10000):
    # Unpack states
    [x, y, vx, vy, lambda_1, lambda_2, lambda_3, lambda_4] = states

    # Atmospheric parameters
    #planet_atmo = planetary_model.atmo
    # Find gravitational acceleration
    pl_rad = 6378
    mu = 398600
    #g = 1000 * mu/((y/1000 + pl_rad)**2)
    g = 3.986e14/(y**2)

    # Find mach and flight path angle
    speed_of_sound = 343
    V = np.sqrt(vx**2 + vy**2)
    M = V/speed_of_sound

    #TODO: Drag
    Cd = 1.0
    A_ref = np.pi * 9
    rho_ref = 1.225;
    h_sc = 100000


    # Equations of motions

    # Parameters of interest (written to simplify code)
    arg = np.sqrt(lambda_3**2 + lambda_4**2)
    cosd_alpha = -lambda_3/arg
    sind_alpha = lambda_4/arg
    k1 = rho_ref * Cd * A_ref/(2 * m)

    # Physical EOMS
    dxdt = vx                                                                                 # x-EOM
    dydt = vy                                                                                 # y-EOM
    dvxdt = Thrust/m * lambda_3/arg - k1 * np.exp(-y/h_sc) * vx * np.sqrt(vx**2 + vy**2)      # vx-EOM
    dvydt = Thrust/m * lambda_4/arg + k1 * np.exp(-y/h_sc) * vy * np.sqrt(vx**2 + vy**2)      # vy-EOM

    # Co-states (arises from Calculus of Variations. Ref: Brysan & Ho or Longuski et. Al.)
    l1_dot = 0
    l2_dot = k1/h_sc * np.exp(-y/h_sc) * ((lambda_4 * vy - lambda_3 * vx)/np.sqrt(vx**2 + vy**2))
    arg_l3 = -lambda_3 * vy**2/((vx**2 + vy**2)**1.5) - lambda_4 * vy*vx/((vx**2 + vy**2)**1.5)
    l3_dot = -(lambda_1 + k1 * np.exp(-y/h_sc) * arg_l3)
    arg_l4 = lambda_4 * vx**2/((vx**2 + vy**2)**1.5) + lambda_3 * vx * vy/((vx**2 + vy**2)**1.5)
    l4_dot = -(lambda_2 + k1 * np.exp(-y/h_sc) * arg_l4)

    return [dxdt, dydt, dvxdt, dvydt, l1_dot, l2_dot, l3_dot, l4_dot]
