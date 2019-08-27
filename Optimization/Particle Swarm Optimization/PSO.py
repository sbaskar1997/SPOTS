#!/usr/bin/env python

# Particle Swarm Optimization
# See https://en.wikipedia.org/wiki/Particle_swarm_optimization for more info
# Author: Sandeep Baskar

# Import native modules
import numpy as np
import sys
import os
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d

# Append appropriate directories
sys.path.append(os.path.join('../../common/math'))

# Import custom modules
from vectormath import *
from Swarm import Swarm
from ObjectiveFunction import objective_function

# Initialization of problem
swarm = Swarm(number_of_particles = 100)
n_iterations = 500
n_var = 2
upper_bounds = np.array([10, 10])
lower_bounds = np.array([-10, -10])
GBEST = np.zeros(n_iterations)
particle_state_history = np.zeros(shape = (n_iterations, len(swarm.particles)))
particle_velocity_history = np.zeros(shape = (n_iterations, len(swarm.particles)))

# Change inertia weights until convergence
w_max = 0.9
w_min = 0.2
w = np.linspace(w_max, w_min, n_iterations)

# Cognitive and social weights (c1 and c2 respectively)
c1 = 2
c2 = 2


# Initialize particles
for particle in range(0, len(swarm.particles)):
    gen_x = (upper_bounds - lower_bounds) * rand(n_var) + lower_bounds
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
    # Loop through each particles
    for p in range(0,len(swarm.particles)):
        current_state = swarm.particles[p].X

        current_state = (upper_bounds - lower_bounds) * rand(n_var) + lower_bounds
        particle_state_history[it, p] = current_state
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
        inertia_term = w[it] * swarm.particles[p].V
        inertia_term = w[it] * swarm.particles[p].V
        r1 = rand(n_var)

        # Cognitive term
        cognitive_term_1 = c1 * r1
        cognitive_term_2 = swarm.particles[p].best_X - swarm.particles[p].X
        cognitive_term = cognitive_term_1 * cognitive_term_2


        # Social term
        r2 = rand(n_var)
        social_term_1 = c2 * r2
        social_term_2 = swarm.best_X - swarm.particles[p].X
        social_term = social_term_1 * social_term_2

        # Add all terms together
        V_next = inertia_term + cognitive_term + social_term
        particle_velocity_history[it, p] = V_next
        X_next = swarm.particles[p].X + V_next

        # Update particle position and velocity
        swarm.particles[p].X = X_next
        swarm.particles[p].V = V_next

    GBEST[it] = swarm.best_O

it_vec = np.linspace(1,n_iterations + 1, n_iterations)
plt.plot(it_vec, GBEST)
plt.show()

#draw_landscape(objective_function, upper_bounds, lower_bounds)
draw_particles(objective_function, upper_bounds, lower_bounds, swarm)
