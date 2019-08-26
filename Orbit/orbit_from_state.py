#!/usr/bin/env python
# Python function that will return orbit from given state vectors
# Author: Sandeep Baskar

import numpy as np
from Orbit import Orbit

def orbit_from_state(pos, vel, center_body_mu = 398600):
    # Cast vectors into numpy arrays for computational ease
    pos_inertial = np.array(pos)
    vel_inertial = np.array(vel)

    # Find magnitudes of position and velocity
    pos_mag = np.linalg.norm(pos_inertial)
    vel_mag = np.linalg.norm(vel_inertial)

    # Angular momentum
    angular_momentum_vector_inertial = np.cross(pos_inertial, vel_inertial)
    angular_momentum_mag = np.linalg.norm(angular_momentum_vector_inertial)
    h_hat = angular_momentum_vector_inertial/angular_momentum_mag
    line_of_nodes_vec = np.cross([0,0,1], angular_momentum_vector_inertial)

    # Flight path angles (double signed) (radians)
    gam_1 = np.arccos(angular_momentum_mag / (pos_mag * vel_mag))
    gam_2 = -np.arccos(angular_momentum_mag / (pos_mag * vel_mag))

    # Energy
    eps = np.linalg.norm(vel_inertial)**2/2 - center_body_mu/np.linalg.norm(pos_inertial)

    # Semi-Major Axis
    a = -center_body_mu / (2 * eps)

    # Eccentricity
    term_1 = (pos_mag * vel_mag**2 / center_body_mu - 1)**2
    ecc = np.sqrt(term_1 * np.cos(gam_1)**2 + np.sin(gam_1)**2)
    ecc_vec = ((vel_mag**2 - center_body_mu/pos_mag) * pos_inertial - np.dot(pos_inertial, vel_inertial) * vel_inertial) / center_body_mu

    if (ecc >= 1):
        print('Orbit is not closed')
        return -1

    # True anomaly
    num = a * (1 - ecc**2)/pos_mag - 1
    theta_star = np.arccos(num/ecc)

    # Inclination (projection of h onto z axis)
    inc = np.arccos(angular_momentum_vector_inertial[2]/angular_momentum_mag) * 180/np.pi

    # Right angle to ascending node
    omega = np.arccos(line_of_nodes_vec[0]/np.linalg.norm(line_of_nodes_vec)) * 180/np.pi

    if(line_of_nodes_vec[1]):
        omega = 360 - omega

    # Argument of perigee
    AOP = np.arccos(np.dot(line_of_nodes_vec, ecc_vec)/(np.linalg.norm(line_of_nodes_vec) * ecc))

    if (ecc_vec[2] < 0):
        AOP = 360 - AOP

    # Generate orbit object
    orbit = Orbit(eccentricity = ecc, semiMajorAxis = a, inclination = inc, raan = omega, aop = AOP)

    return orbit
