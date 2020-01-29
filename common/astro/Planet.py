#!/usr/bin/env python

# Class to make planet
# Author: Sandeep Baskar

# Add native modules
import sys, os
import numpy as np

class Planet:
    def __init__(self, name, radius_km, mu, atmo_model, km = True):
        self.name = name
        if km:
            self.radius = radius_km
            self.mu = mu
        else:
            self.radius = radius_km * 1000
            self.mu = mu * 1e9
        self.atmo_model = atmo_model
        self.rho_ref = self.atmo_model(0)[-1]
