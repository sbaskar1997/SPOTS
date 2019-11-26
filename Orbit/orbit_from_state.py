#!/usr/bin/env python
# Python function that will return orbit from given state vectors
# Author: Sandeep Baskar

# Import native modules
import numpy as np
import math
import sys, os
import scipy.optimize as opt

# Import custom modules
sys.path.insert(0, os.path.abspath('..'))
from Orbit import Orbit
from common.math.vectormath import nearly_equal

def orbit_from_pos_vel(pos, vel, center_body_mu = 398600):
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


    # Check for NaN values for orbital elements
    if (ecc_vec[2] < 0):
        AOP = 360 - AOP

    if (math.isnan(AOP)):
        AOP = 0

    if (math.isnan(omega)):
        omega = 0

    if (math.isnan(inc)):
        inc = 0

    # Generate orbit object
    orbit = Orbit(eccentricity = ecc, semiMajorAxis = a, inclination = inc, raan = omega, aop = AOP)

    return orbit

def orbit_from_pos_pos_p(r_1, r_2, p, mu = 398600):
    # Changing vectors to numpy arrays to increase computational efficiency
    r_1 = np.array(r_1)
    r_2 = np.array(r_2)

    # Find magnitudes of both vectors
    r_1_mag = np.linalg.norm(r_1)
    r_2_mag = np.linalg.norm(r_2)

    # Solve for angular momentum
    h_hat = np.cross(r_1, r_2)/np.linalg.norm(np.cross(r_1, r_2))

    # Use vector 1 for DCM resolution to find orbital parameters
    r_1_hat = r_1/r_1_mag

    # h_hat cross r_1_hat will yield theta_1 hat by RHR
    theta_1_hat = np.cross(h_hat, r_1_hat)

    # Forming DCM
    DCM = np.matrix([r_1_hat, theta_1_hat, h_hat]).transpose()

    # Check to see if matrix is 2d
    if (DCM[0,2] == 0 and DCM[1,2] == 0 and DCM[2,0] == 0 and DCM[2,1] == 0):
        two_dim = True

    # Find Inclination
    inc = np.arccos(DCM[2,2]) * 180/np.pi
    if (inc < 0):
        inc = -inc

    # Find RAAN
    o1_1 = np.arcsin(DCM[0,2]/np.sin(np.radians(inc))) * 180/np.pi
    o1_2 = 180 - o1_1
    omega_1 = [o1_1, o1_2]

    o2_1 = np.arccos(-DCM[1,2]/np.sin(np.radians(inc))) * 180/np.pi
    omega_2 = [o2_1, -o2_1]

    omega = -1
    for omega1 in omega_1:
        for omega2 in omega_2:
            try:
                if nearly_equal(omega1, omega2):
                    omega = omega1
            except:
                omega = 0

    # Find longitudinal anomaly
    ta_1 = np.arcsin(DCM[2,0]/np.sin(np.radians(inc))) * 180/np.pi
    ta_2 = 180 - ta_1
    theta_a = [ta_1, ta_2]

    tb_1 = np.arccos(DCM[2,1]/np.sin(np.radians(inc))) * 180/np.pi
    theta_b = [tb_1, -tb_1]

    theta_1 = -1
    for thetaA in theta_a:
        for thetaB in theta_b:
            try:
                if nearly_equal(thetaA, thetaB):
                    theta_1 = thetaA
            except:
                theta_1 = 0


    # Find f and g functions
    d_theta_star = np.arccos(np.dot(r_1, r_2)/(r_1_mag * r_2_mag)) * 180/np.pi
    f = 1 - r_2_mag/p * (1 - np.cos(np.radians(d_theta_star)))
    g = r_1_mag * r_2_mag/np.sqrt(mu * p) * np.sin(np.radians(d_theta_star))

    # Find velocity vector assoc. with r_1 vector
    v_1 = (r_2 - f * r_1) * 1/g

    # Find whether satellite is ascending or descending (sign of Flight path angle)
    FPA_sign = 1
    r1_dot = np.dot(v_1, r_1)/r_1_mag
    if r1_dot < 0:
        FPA_sign = -1

    # Find remaining orbital elements
    v_1_mag = np.linalg.norm(v_1)
    sp_en = v_1_mag**2/2 - mu/r_1_mag

    # Semi-major axis
    a = -mu/(2 * sp_en)

    # Eccentricity
    ecc = np.sqrt(1 - p/a)

    # True anomalies
    theta_1_star = FPA_sign * np.arccos(1/ecc * (p/r_1_mag - 1)) * 180/np.pi
    theta_2_star = theta_1_star + d_theta_star

    # Argument of perigee
    AOP = theta_1 - theta_1_star

    # Create orbit object
    orbit = Orbit(eccentricity = ecc, semiMajorAxis = a, inclination = inc, raan = omega, aop = AOP)

    # Return orbit and two true anomalies
    return [orbit, theta_1_star, theta_2_star]
