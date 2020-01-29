#!/usr/bin/env python

# Creates Earth instance
# Author: Sandeep Baskar

# Import native modules
import numpy as np
import sys, os

# Add root directory of SPOTS
sys.path.insert(0, os.path.abspath('../..'))
from common.astro.Planet import Planet
from common.astro.planets.earth import *
from common.astro.planets.mars import *

def earth(km = True):
    earth = Planet('earth', 6378, 398600, earth_atmo, km = km)
    return earth

def mars(km = True):
    mars = Planet('mars', 3389.5, 0.042828e6, mars_atmo, km = km)
    return mars
