# Python Class that will take orbital elements

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
