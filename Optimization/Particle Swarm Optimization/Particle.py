#!/usr/bin/env python

# Python class that describes a particle
# Author: Sandeep Baskar

class Particle:
    def __init__(self, id, current_X, current_V):
        self._id = id
        self._X = current_X
        self._V = current_V
        self._best_X = None
        self._best_V = None

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
    def best_V(self, val):
        self._best_V = val
