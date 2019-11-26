#!usr/bin/env python
# Author: Sandeep Baskar
# Lambert Solver: Time of Flight Orbit Determination
# Import native modules
import numpy as np
import matplotlib.pyplot as plt
import sys, os
import scipy.optimize as opt

# Import custom modules
sys.path.insert(0, os.path.abspath('..'))
from Orbit import *
from common.math.vectormath import *
from orbit_from_state import orbit_from_pos_pos_p


def lambert_solver(r_1, r_2, TOF):
    # Re-factor parameters to be numpy friendly
    r_1 = np.array(r_1)
    r_2 = np.array(r_2)

    # Additional parameters needed for analysis
    r_1_mag = np.linalg.norm(r_1)
    r_2_mag = np.linalg.norm(r_2)
    mu = 398600                     # TODO: Parameterize this in functional **kwargs

    # Solve for angle between r_1 and r_2 (Transfer angle)
    phi = angle_between_vecs(r_1, r_2)

    # Solve for space triangle parameters
    c = np.sqrt(r_1_mag**2 + r_2_mag**2 - 2 * r_1_mag * r_2_mag * np.cos(np.radians(phi)))
    s = 0.5 * (r_1_mag + r_2_mag + c)

    # Check minimum energy path (assume elliptical orbit)
    a_min = s/2
    alpha_0 = 2 * np.arcsin(np.sqrt(s/(2*a_min)))
    alpha_0_deg = alpha_0 * 180/np.pi
    beta_0 = 2 * np.arcsin(np.sqrt((s - c)/(2*a_min)))
    beta_0_deg = beta_0 * 180/np.pi
    TOF_min = np.sqrt(a_min**3/mu) * ((alpha_0 - np.sin(alpha_0)) - (beta_0 - np.sin(beta_0)))
    beta = -1

    # Solve for alpha and beta angles depending on type
    if (TOF > TOF_min):
        # Type B
        type = 'b'
        alpha = 2*np.pi - alpha_0
        beta = beta_0
    else:
        # Type A
        type = 'a'
        alpha = alpha_0

    p = -1

    # Iterate on a until it matches time of flight
    def zerofun(guess):
        [a_guess] = guess
        # Based off guessed semi-major axis, solve for orbit
        sp_en = -mu/(2 * a_guess)
        v1 = np.sqrt(2 *(sp_en + mu/r_1_mag))

        # Solve for alpha_0 and beta_0
        alpha_0 = 2 * np.arcsin(np.sqrt(s/(2*a_guess)))
        beta_0 = 2 * np.arcsin(np.sqrt((s - c)/(2 * a_guess)))

        if (type == 'b'):
            alpha = 2 * np.pi - alpha_0
            beta = beta_0
        else:
            alpha = alpha_0
            beta = 2*np.pi - beta_0

        # Solve for semi-latus rectum
        p1 = 4 * a_guess * (s - r_1_mag) * (s - r_2_mag)/(c**2) * (np.sin((alpha + beta)/2)**2)
        p2 = 4 * a_guess * (s - r_1_mag) * (s - r_2_mag)/(c**2) * (np.sin((alpha - beta)/2)**2)
        p_choices = [p1, p2]

        # Pick appropriate p value based off orbit type
        if (type == 'b'):
            p = np.amin(p_choices)
        else:
            p = np.amax(p_choices)

        # Find eccentricity
        ecc = np.sqrt(1 - p/a_guess)

        argz = 2 * np.pi - (alpha_0 - np.sin(alpha_0)) + (beta_0 - np.sin(beta_0))
        rhs = a_guess**(1.5) * argz
        TOF_guess = rhs/np.sqrt(mu)

        return [TOF_guess - TOF]

    [a_act] = opt.fsolve(zerofun, a_min)

    # Solve for alpha_0 and beta_0
    alpha_0 = 2 * np.arcsin(np.sqrt(s/(2*a_act)))
    beta_0 = 2 * np.arcsin(np.sqrt((s - c)/(2 * a_act)))

    if (type == 'b'):
        alpha = 2 * np.pi - alpha_0
        beta = beta_0
    else:
        alpha = alpha_0
        beta = 2*np.pi - beta_0

    # Solve for semi-latus rectum
    p1 = 4 * a_act * (s - r_1_mag) * (s - r_2_mag)/(c**2) * (np.sin((alpha + beta)/2)**2)
    p2 = 4 * a_act * (s - r_1_mag) * (s - r_2_mag)/(c**2) * (np.sin((alpha - beta)/2)**2)
    p_choices = [p1, p2]
    p = -1



    # Pick appropriate p value based off orbit type
    if (type == 'a'):
        p = np.amax(p_choices)
    else:
        p = np.amin(p_choices)

    # Get orbit from semi latus rectum and two position vectors
    [orbit, theta_1_star, theta_2_star] = orbit_from_pos_pos_p(r_1, r_2, p)

    return orbit
