#!/usr/bin/python3
"""
Created by Hannes Bergström 18/11/21,
modified by Peter Halldestam 20/1/22.

Generates DREAM settings files of different inverse aspect ratios "epsilon".

Effect of toroidicity, reproduction of fig. 6 in paper:
(E Nilsson et al 2015 Plasma Phys. Control. Fusion 57 095006)
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../../../..'))
import parameters as p

# helper function import
sys.path.append(os.path.join(dir, '../../..'))
from configureDREAM import ConfigureDREAM
from configureDREAM import CYLINDRICAL, TOROIDAL

# import formula
sys.path.append(p.DREAM_PATH)
from DREAM.Formulas.PlasmaParameters import getEc

# tokamak geometry
a = 0.8 * p.MAJOR_RADIUS    # minor radius
b = 1.2 * a                 # wall radius

# plasma parameters
T = 5e2               # temperature
n = 2e19#p.ELECTRON_DENSITY      # plasma density
E = 40 * getEc(T, n)        # Connor-Hastie critical electric field
# print(14.9 - 0.5*np.log(n / 1e20) + np.log(T / 1e3))

n_e = p.ELECTRON_DENSITY
c = 299792458
q = 1.6e-19
lnC = 4
epsilon_0 = 8.85e-12
m_0 = 9.1e-31

E_field = 40 * n_e * q**3 * lnC / (4*np.pi * epsilon_0**2 * m_0 * c**2)
# print(E, E_field)
#
# E=E_field
if __name__ == "__main__":

    ConfigureDREAM(include='fluid',
                   temperature=T, electricField=E,
                   geometry=CYLINDRICAL, wallRadius=b,
                   minorRadius=a, verbose=(len(sys.argv)==2),
                   output=f'outputs/output_cyl.h5',
                   save=f'settings/setting_cyl.h5')


    ConfigureDREAM(include='fluid',
                   temperature=T, electricField=E,
                   geometry=TOROIDAL, wallRadius=b,
                   minorRadius=a, verbose=(len(sys.argv)==2),
                   output=f'outputs/output_tor.h5',
                   save=f'settings/setting_tor.h5')
