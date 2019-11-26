#!/usr/bin/env python
# Python Class that will take orbital elements and provide orbital information
# Author: Sandeep Baskar

# Import required modules
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Helper functions
def c(arg):
    return np.cos(np.radians(arg))

def s(arg):
    return np.sin(np.radians(arg))

# Function to do matrix multiplication of 3x3 with 3x1
def matmul(a,b):
    [C11, C12, C13] = a[0][:]
    [C21, C22, C23] = a[1][:]
    [C31, C32, C33] = a[2][:]
    R1 = C11 * b[0] + C12 * b[1] + C13 * b[2]
    R2 = C21 * b[0] + C22 * b[1] + C23 * b[2]
    R3 = C31 * b[0] + C32 * b[1] + C33 * b[2]
    return [R1, R2, R3]

class Orbit:
    # Class constructor
    def __init__(self, eccentricity, semiMajorAxis, inclination, raan, aop):
        self.eccentricity = eccentricity
        self.semiMajorAxis = semiMajorAxis
        self.inclination = inclination
        self.raan = raan
        self.aop = aop


    # Calculate semi-latus rectum
    @property
    def semiLatusRectum(self):
        self._semiLatusRectum = self.semiMajorAxis * (1 - self.eccentricity**2)
        return self._semiLatusRectum

    # Calculate radial coordinates of spacecraft in orbit
    @property
    def r(self):
        P = self.semiLatusRectum
        self._r = np.zeros((360,))
        for thetaStar in range(360):
            self._r[thetaStar] = P/(1 + self.eccentricity * np.cos(np.radians(thetaStar)))
        return self._r

    # Calculate directional cosine matrix at a particular true anomaly relating
    # orbital and inertial frames
    def _dcm(self, thetaStar):
        theta = thetaStar + self.aop
        inc = self.inclination
        omega = self.raan
        C11 = c(omega) * c(theta) - s(omega) * c(inc) * s(theta)
        C12 = -c(omega) * s(theta) - s(omega) * c(inc) * c(theta)
        C13 = s(omega) * s(inc)
        C21 = s(omega) * c(theta) + c(omega) * c(inc) * s(theta)
        C22 = -s(omega) * s(theta) + c(omega) * c(inc) * c(theta)
        C23 = -c(omega) * s(inc)
        C31 = s(inc) * s(theta)
        C32 = s(inc) * c(theta)
        C33 = c(inc)
        C = [[C11, C12, C13],[C21, C22, C23],[C31, C32, C33]]
        return C

    # Calculate inertial (J2000) coordinates at every true anomaly position
    def _inertial_vec(self):
        _r_inertial = self.r
        self._rVectorInertial = np.zeros((360,3))

        # Iterate through true anomaly to find (x,y,z) coordinates
        for _thetaStar in range(0,360):
            # Find coordinates in orbit fixed reference frame
            _theta = _thetaStar + self.aop
            _rVectorOrbital = [_r_inertial[_thetaStar], _theta, 0]

            # Calculate DCM at each true anomaly
            _DCM = self._dcm(_thetaStar)

            # Calculate inertial coordinates
            self._rVectorInertial[_thetaStar][:] = matmul(_DCM, _rVectorOrbital)

        return self._rVectorInertial

    # Get inertial x values
    @property
    def x(self):
        _rVectorInertial = self._inertial_vec()
        self._x = _rVectorInertial[:,0]
        return self._x

    # Get inertial y values
    @property
    def y(self):
        _rVectorInertial = self._inertial_vec()
        self._y = _rVectorInertial[:,1]
        return self._y

    # Get inertial z values
    @property
    def z(self):
        _rVectorInertial = self._inertial_vec()
        self._z = _rVectorInertial[:,2]
        return self._z

    # Static method to setup plot
    def plot(self):
        x = self.x
        y = self.y
        z = self.z

        # Initializing 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')

        # Plot orbit
        ax.plot(x, y, z)

        # Initializing Earth
        r_earth = 6378
        u = np.linspace(0, np.pi, 30)
        v = np.linspace(0, 2 * np.pi, 30)

        x_e = np.outer(np.sin(u), np.sin(v)) * r_earth
        y_e = np.outer(np.sin(u), np.cos(v)) * r_earth
        z_e = np.outer(np.cos(u), np.ones_like(v)) * r_earth

        # Plot earth
        ax.plot_wireframe(x_e, y_e, z_e)

        plt.show()
        return fig
