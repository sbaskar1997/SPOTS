#!/usr/bin/env python

# Creates Earth atmosphere model
# Author: Sandeep Baskar

# Import native modules
import numpy as np

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
