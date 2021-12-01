#!/usr/bin/python3
"""
Created by Hannes Bergström 18/11/21.

Generates DREAM settings files of different inverse aspect ratios "epsilon".
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../../../..'))
from parameters import MAJOR_RADIUS, ELECTRON_DENSITY

# helper function import
sys.path.append(os.path.join(dir, '../../..'))
from configureDREAM import ConfigureDREAM
# Geometries
from DREAM.Settings.RadialGrid import TYPE_CYLINDRICAL as CYLINDRICAL
from DREAM.Settings.RadialGrid import TYPE_ANALYTIC_TOROIDAL as TOROIDAL
 

mR = 0.9 * MAJOR_RADIUS
wR = 1.2*mR

T = 500

n_e = ELECTRON_DENSITY
c = 299792458
q = 1.6e-19
lnC = 4
epsilon_0 = 8.85e-12
m_0 = 9.1e-31

E_field = 40 * n_e * q**3 * lnC / (4*np.pi * epsilon_0**2 * m_0 * c**2)

if __name__ == "__main__":

    ConfigureDREAM(include=['fluid/runawayRate', 'fluid/gammaDreicer'],
                   temperature=T, electricField=E_field,
                   geometry=CYLINDRICAL, wallRadius=wR,
                   minorRadius=mR, verbose=(len(sys.argv)==2),
                   output=f'outputs/output_cyl.h5',
                   save=f'settings/setting_cyl.h5')


    ConfigureDREAM(include=['fluid/runawayRate', 'fluid/gammaDreicer'],
                   temperature=T, electricField=E_field,    
                   geometry=TOROIDAL, wallRadius=wR,
                   minorRadius=mR, verbose=(len(sys.argv)==2),
                   output=f'outputs/output_tor.h5',
                   save=f'settings/setting_tor.h5')
