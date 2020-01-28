#!usr/bin/env python
# Author: Sandeep Baskar
# File that will take a nominal orbit and add random perturbations along discretized time steps and output change in orbital elements

# Import native modules
import numpy as np
import sys, os
import matplotlib.pyplot as plt
import random
import math

# Import custom modules
sys.path.insert(0, os.path.abspath('..'))
from Orbit.Orbit import Orbit
from Orbit.lambert_solver import *


# Create equatorial orbit
reference_orbit = Orbit.Orbit(eccentricity = 0, semiMajorAxis = 200 + 6378, inclination = 0, raan = 0, aop = 0)
r_vec_act = np.zeros((360, 3))
E_array = np.array([])
theta_star = 0
mu = 398600
margin = 0.01

# Perturb each position vector
for vec in reference_orbit.r_vec:
    r_vec_act[theta_star, 0] = vec[0] + random.uniform(-margin, margin) * vec[0]
    r_vec_act[theta_star, 1] = vec[1] + random.uniform(-margin, margin) * vec[1]
    r_vec_act[theta_star, 2] = vec[2] + random.uniform(-margin, margin) * vec[2]


    # Find eccentric anomalies at each point and find time of flight associated
    E_curr = 2 * np.arctan((1 + reference_orbit.eccentricity)/(1 - reference_orbit.eccentricity)**2 * np.tan(np.radians(theta_star/2))) * 180/np.pi
    if E_curr < 0:
        E_curr = E_curr + 360
    E_array = np.append(E_array, E_curr)

    # Increment theta_star
    theta_star = theta_star + 1

# Initialize delta parameters
d_omega = np.zeros((359,1))
d_aop = np.zeros((359,1))
d_ecc = np.zeros((359,1))
d_a = np.zeros((359,1))

# Loop through each time step and find change in orbital parameters
for i in range(1, len(r_vec_act - 1)):
    r_1 = r_vec_act[i - 1]
    r_2 = r_vec_act[i]

    # Find Time of flight based off of nominal orbit
    E_0 = np.radians(E_array[i - 1])
    E_c = np.radians(E_array[i])
    TOF = np.sqrt(reference_orbit.semiMajorAxis**3/mu) * (E_c - E_0 - reference_orbit.eccentricity * (np.sin(E_c) - np.sin(E_0)))

    # Use lambert solver and populate all deltas
    orbit_act = lambert_solver(r_1, r_2, TOF)
    print(orbit_act.semiMajorAxis)
