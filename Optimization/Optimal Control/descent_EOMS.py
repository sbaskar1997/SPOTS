#!/usr/bin/env python

# Optimal Control EOMS for descent trajectory (2D analysis, flat planet)
# Author: Sandeep Baskar

'''TODO:
    Need to write planetary model (do temp earth in this file)
    Need to write mathematical functions for cosd and sind
    Need to update drag model
'''

# Import native modules
import numpy as np

def earth_atmo(alt):
    return alt + 5;

def EOM_ascent(states, altitude, planetary_model = earth_model, Thrust = 100000):
    # Unpack states
    [x, y, vx, vy, lambda_1, lambda_2, lambda_3, lambda_4] = states

    # Center body parameters
    mu = earth_model.mu
    r_planet = earth_mode.radius

    # Atmospheric parameters
    planet_atmo = planetary_model.atmo
    [T, p, rho] = planet_atmo(y)

    # Find gravitational acceleration
    g = 1000 * mu/((y/1000 + 6378)**2)

    # Find mach and flight path angle
    speed_of_sound = planet_atmo.a
    V = np.sqrt(vx**2 + vy**2)
    M = V/speed_of_sound
    if x != 0:
        theta = np.degrees(np.arctan(y/x))
    else:
        theta = 0

    #TODO: Drag
    D = 50000

    # Equations of motions

    # Parameters of interest (written to simplify code)
    arg = np.sqrt(lambda_3**2 + lambda_4**2)
    cosd_alpha = -lambda_3/arg
    sind_alpha = lambda_4/arg

    # Physical EOMS
    dxdt = vx                                                   # x-EOM
    dydt = vy                                                   # y-EOM
    dvxdt = 1/m * (-D * cosd(theta) - Thrust * cosd_alpha)      # vx-EOM
    dvydt = 1/m * (D * sind(theta) - Thrust * sind_alpha)       # vy-EOM

    # Co-states (arises from Calculus of Variations. Ref: Brysan & Ho or Longuski et. Al.)
    l1_dot = 0
    if (lambda_3**2 + lambda_4**2 == 0):
        l2_dot = 0
        l3_dot = 0
        l4_dot = -lambda_2
    else:
        l2_dot = 0
        l3_dot = -lambda_1
        l4_dot = -lambda_2

    return [dxdt, dydt, dvxdt, dvydt, l1_dot, l2_dot, l3_dot, l4_dot]
