#!/usr/bin/env python

# Particle Swarm Optimization
# See https://en.wikipedia.org/wiki/Particle_swarm_optimization for more info
# Author: Sandeep Baskar

# Import native modules
import numpy as np
import sys
import os
import random

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

# Cognitive and social weights (c1 and c2 respectively)
c1 = 2
c2 = 2

# Initialize particles
for particle in range(0, len(swarm.particles)):
    gen_x = element_add(
                element_multiply(
                    element_subtract(upper_bounds, lower_bounds),
                    rand(n_var))
                , lower_bounds)
    zeros_vec = zeros(n_var)


    swarm.particles[particle].X = gen_x
    swarm.particles[particle].V = zeros_vec
    swarm.particles[particle].best_X = zeros_vec
    swarm.particles[particle].best_O = float('inf')

# Initialize swarm attributes for global optimum
swarm.best_O = float('inf')
swarm.best_X = zeros(n_var)

# Main iteration loop
for it in range(0,n_iterations):
    print(it)
    # Loop through each particles
    for p in range(0,len(swarm.particles)):
        current_state = swarm.particles[p].X
        if (current_state == 0):
            current_state = element_add(
                        element_multiply(
                            element_subtract(upper_bounds, lower_bounds),
                            rand(n_var))
                        , lower_bounds)
            swarm.particles[p].X = current_state

        current_objective_cost = objective_function(current_state)

        # Check if current objective cost is lower than best objective cost (local)
        if (current_objective_cost < swarm.particles[p].best_O):
            swarm.particles[p].best_O = current_objective_cost
            swarm.particles[p].best_X = current_state

        # Check if current objective cost is lower than best objective cost (global)
        if (current_objective_cost < swarm.best_O):
            swarm.best_O = current_objective_cost
            swarm.best_X = current_state

    # Update next time step
    for p in range(0,len(swarm.particles)):
        # Inertia term
        inertia_term = scalar_multiply(w[it], swarm.particles[p].V)
        r1 = rand(n_var)

        # Cognitive term
        cognitive_term_1 = scalar_multiply(c1, r1)
        cognitive_term_2 = element_subtract(swarm.particles[p].best_X, swarm.particles[p].X)
        cognitive_term = element_multiply(cognitive_term_1, cognitive_term_2)

        # Social term
        r2 = rand(n_var)
        social_term_1 = scalar_multiply(c2, r2)
        social_term_2 = element_subtract(swarm.best_X, swarm.particles[p].X)
        social_term = element_multiply(social_term_1, social_term_2)

        # Add all terms together
        V_next = element_add(element_add(inertia_term, cognitive_term), social_term)
        X_next = element_add(swarm.particles[p].X, V_next)

        # Update particle position and velocity
        swarm.particles[p].X = X_next
        swarm.particles[p].V = V_next
