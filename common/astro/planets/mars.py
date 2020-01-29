#!/usr/bin/env python

# Creates Mars atmospheric model
# Author: Sandeep Baskar

# Import native modules
import numpy as np

def mars_atmo(alt):
    if alt > 7000:
        T = -23.4 - .00222 * alt
        p = .699 * np.exp(-.00009 * alt)
    else:
        T = -31 - .000998 * alt
        p = .699 * np.exp(-0.00009 * alt)

    rho = p/(.1921 * (T + 273.15))

    return [T + 273.15, p * 1000, rho]
