#!/usr/bin/env python

# Python class that will generate a swarm of particles, given number of particles
# Author: Sandeep Baskar

# Import required modules
from Particle import Particle

class Swarm:
    def __init__(self, number_of_particles = 100):
        self._number_of_particles = number_of_particles
        self._particles = []
        self._best_X = float('inf')
        self._best_V = float('inf')

    @property
    def particles(self):
        # Generate particles
        for i in range(0,self._number_of_particles):
            random_v_val = 0
            random_x_val = 0
            self._particles.append(Particle(id = i, current_X = random_x_val,
                                   current_V = random_v_val))

        return self._particles

    @property
    def best_X(self):
        return self._best_X

    @best_X.setter
    def best_X(self, val):
        self._best_X = val

    @property
    def best_V(self):
        return self._best_V

    @best_V.setter
    def best_V(self,val):
        self._best_V = val
