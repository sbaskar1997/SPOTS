#!/usr/bin/env python

# File with helper functions for vector math
# Author: Sandeep Baskar

# Import required modules
import random
import numpy as np

def rand(length):
    return np.random.random_sample(length)

def zeros(length):
    return np.zeros(length)

def nearly_equal(a,b,sig_fig=5):
    return ( a==b or 
             int(a*10**sig_fig) == int(b*10**sig_fig)
           )
