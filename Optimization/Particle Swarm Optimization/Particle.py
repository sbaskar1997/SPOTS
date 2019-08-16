#!/usr/bin/env python

# Python class that describes a particle
# Author: Sandeep Baskar

class Particle:
    def __init__(self, id, current_X, current_V):
        self._id = id
        self.X = current_X
        self.V = current_V
        self._best_X = None
        self._best_O = float('inf')

    @property
    def best_X(self):
        return self._best_X

    @best_X.setter
    def best_X(self, val):
        self._best_X = val

    @property
    def best_O(self):
        return self._best_O

    @best_O.setter
    def best_O(self, val):
        self._best_O = val
