#!/usr/bin/env python

# Particle Swarm Optimization
# See https://en.wikipedia.org/wiki/Particle_swarm_optimization for more info
# Author: Sandeep Baskar

# Import native modules
import numpy as np
import sys
import os

# Append appropriate directories
sys.path.append(os.path.join('../../common/math'))

# Import custom modules
from vectormath import *
from Swarm import Swarm


def objective_function(X):
    # TODO: Make your own objective function here
    o = sum(square_vector(X))
    return o



swarm = Swarm(number_of_particles = 100)
n_iterations = 500
n_var = 2
upper_bounds = [10, 10]
lower_bounds = [-10, -10]

# Change inertia weights until convergence
w_max = 0.9
w_min = 0.2
w = np.linspace(w_max, w_min, n_iterations)

# Initialize
