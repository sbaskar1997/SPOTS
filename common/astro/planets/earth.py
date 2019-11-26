#!/usr/bin/env python

# Creates Earth instance
# Author: Sandeep Baskar

# Import native modules
import numpy as np

def earth_atmo(y):
    if y > (25000/1000):
        T = -131.21 + .00299 * y
        p = 2.488 * ((T + 273.15)/216.6)**-11.388

    if ((y > 11000/1000) && (y <= 25000/1000)):
        T = -56.46
        p = 22.65 * np.exp(1.73 - .000157 * (y * 1000))

    else:
        T = 15.04 - .00649 * y * 1000
