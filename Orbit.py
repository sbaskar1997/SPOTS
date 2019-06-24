# Python Class that will take orbital elements
# Author: Sandeep Baskar

#!/usr/bin/env python

import numpy as np


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
    R1              = C11 * b[0] + C12 * b[1] + C13 * b[2]
    R2              = C21 * b[0] + C22 * b[1] + C23 * b[2]
    R3              = C31 * b[0] + C32 * b[1] + C33 * b[2]
    return [R1, R2, R3]

class Orbit:
    # Class constructor
    def __init__(self, eccentricity, semiMajorAxis, inclination, raan, aop):
        self._eccentricity  = eccentricity
        self._semiMajorAxis = semiMajorAxis
        self._inclination   = inclination
        self._raan          = raan
        self._aop           = aop

    # Eccentricity getter and setter
    @property
    def eccentricity(self):
        return self._eccentricity

    @eccentricity.setter
    def eccentricity(self, val):
        self._eccentricity = val

    # Semimajor axis getter and setter
    @property
    def semiMajorAxis(self):
        return self._getsemiMajorAxis

    @semiMajorAxis.setter
    def semiMajorAxis(self, val):
        self_semiMajorAxis = val

    # Inclination getter and setter
    @property
    def inclination(self):
        return self._inclination

    @inclination.setter
    def inclination(self,val):
        self._inclination = val

    # RAAN getter and setter
    @property
    def raan(self):
        return self._raan

    @raan.setter
    def raan(self,val):
        self._raan = val

    # AOP getter and setter
    @property
    def aop(self):
        return self._aop

    @aop.setter
    def aop(self,val):
        self._aop = val

    # Calculate semi-latus rectum
    @property
    def semiLatusRectum(self):
        self._semiLatusRectum = self._semiMajorAxis * (1 - self._eccentricity**2)
        return self._semiLatusRectum

    # Calculate radial coordinates of spacecraft in orbit
    @property
    def r(self):
        P = self.semiLatusRectum
        self._r = np.zeros((360,))
        for thetaStar in range(360):
            self._r[thetaStar] = P/(1 + self._eccentricity * np.cos(np.radians(thetaStar)))
        return self._r

    # Calculate directional cosine matrix at a particular true anomaly relating
    # orbital and inertial frames
    def _dcm(self, thetaStar):
        theta = thetaStar + self._aop
        inc   = self._inclination
        omega = self._raan
        C11   = c(omega) * c(theta) - s(omega) * c(inc) * s(theta)
        C12   = -c(omega) * s(theta) - s(omega) * c(inc) * c(theta)
        C13   = s(omega) * s(inc)
        C21   = s(omega) * c(theta) + c(omega) * c(inc) * s(theta)
        C22   = -s(omega) * s(theta) + c(omega) * c(inc) * c(theta)
        C23   = -c(omega) * s(inc)
        C31   = s(inc) * s(theta)
        C32   = s(inc) * c(theta)
        C33   = c(inc)
        C     = [[C11, C12, C13],[C21, C22, C23],[C31, C32, C33]]
        return C

    # Calculate inertial (J2000) coordinates at every true anomaly position
    def _inertial_vec(self):
        _r_inertial = self.r
        self._rVectorInertial = np.zeros((360,3))

        # Iterate through true anomaly to find (x,y,z) coordinates
        for _thetaStar in range(0,360):
            # Find coordinates in orbit fixed reference frame
            _theta           = _thetaStar + self.aop
            _rVectorOrbital  = [_r_inertial[_thetaStar], _theta, 0]

            # Calculate DCM at each true anomaly
            _DCM             = self._dcm(_thetaStar)

            # Calculate inertial coordinates
            self._rVectorInertial[_thetaStar][:] = matmul(_DCM, _rVectorOrbital)

        return self._rVectorInertial

    # Get inertial x values
    @property
    def x(self):
        _rVectorInertial = self._inertial_vec()
        return _rVectorInertial[:,0]

    # Get inertial y values
    @property
    def y(self):
        _rVectorInertial = self._inertial_vec()
        return _rVectorInertial[:,1]

    # Get inertial z values
    @property
    def z(self):
        _rVectorInertial = self._inertial_vec()
        return _rVectorInertial[:,2]
