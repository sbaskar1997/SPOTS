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
from mpl_toolkits import mplot3d

# Append appropriate directories
sys.path.append(os.path.join('../../common/math'))

# Import custom modules
from vectormath import *
from Swarm import Swarm
from ObjectiveFunction import objective_function

# Draw 3D landscape
def draw_landscape(landscape_function, upper_bounds, lower_bounds):
    if (len(upper_bounds) > 2):
        print('Warning: More than two dimensions given for landscape,' +
        'only plotting first two variables in search landscape')
    upper_bound_x1 = upper_bounds[0]
    upper_bound_x2 = upper_bounds[1]

    lower_bound_x1 = lower_bounds[0]
    lower_bound_x2 = lower_bounds[1]


    x1 = np.linspace(lower_bound_x1, upper_bound_x1, 200)
    x2 = np.linspace(lower_bound_x2, upper_bound_x2, 200)
    xx, yy = np.meshgrid(x1, x2)

    z = np.zeros(shape = (len(x1), len(x2)))

    for x in range(0,len(x1)):
        for y in range(0,len(x2)):
            z[x,y] = landscape_function(np.array([x1[x], x2[y]]))

    fig = plt.figure()
    ax = plt.axes(projection = '3d')
    ax.plot_surface(xx, yy, z)
    plt.show()

# Draw particle trajectories along 2D plot
def draw_particles(landscape_function, upper_bounds, lower_bounds, swarm):

    # Plot 2D contour
    if (len(upper_bounds) > 2):
        print('Warning: More than two dimensions given for landscape,' +
        'only plotting first two variables in search landscape')

    lower_x = lower_bounds[0]
    lower_y = lower_bounds[1]

    upper_x = upper_bounds[0]
    upper_y = upper_bounds[1]

    x = np.linspace(lower_x, upper_x, 200)
    y = np.linspace(lower_y, upper_y, 200)
    z = np.zeros(shape = (len(x), len(y)))

    xx, yy = np.meshgrid(x,y)

    for x_v in range(0, len(x)):
        for y_v in range(0, len(y)):
            z[x_v, y_v] = landscape_function(np.array([x[x_v], y[y_v]]))

    fig, ax = plt.subplots()
    ax.contour(xx, yy, z)
    plt.show()





# Initialization of problem
swarm = Swarm(number_of_particles = 100)
n_iterations = 500
n_var = 2
upper_bounds = np.array([10, 10])
lower_bounds = np.array([-10, -10])
GBEST = np.zeros(n_iterations)

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
