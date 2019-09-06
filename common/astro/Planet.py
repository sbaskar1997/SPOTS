#!/usr/bin/env python

# Class to make planet
# Author: Sandeep Baskar

class Planet:
    def __init__(self, name, radius_km, star_orbit, atmo_model):
        self.name = name
        self.radius_km = self.radius_km
        self.star_orbit = self.star_orbit
        self.atmo_model = self.atmo_model

    def draw(self):
        self.star_orbit.plot()
