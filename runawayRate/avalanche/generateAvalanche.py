#!/usr/bin/python3
"""
Created by Peter Halldestam 9/12/21

Generates DREAM settings file with FLUID avalanche, with and without trapping correction.

"""
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
from parameters import MAJOR_RADIUS

# helper functiobn import
sys.path.append(os.path.join(dir, '..'))
from configureDREAM import ConfigureDREAM
from configureDREAM import AVALANCHE_FLUID
from configureDREAM import AVALANCHE_TRAPPING_INCLUDE
from configureDREAM import CYLINDRICAL

if __name__ == "__main__":

    a = .9 * MAJOR_RADIUS

    ConfigureDREAM(geometry=CYLINDRICAL,
                   avalanche=AVALANCHE_FLUID,
                   minorRadius=a,
                   wallRadius=1.2*a,
                   include=['fluid/runawayRate', 'fluid/gammaDreicer'],
                   output=f'outputs/baseline.h5',
                   save=f'settings/baseline.h5')

    ConfigureDREAM(avalanche=AVALANCHE_FLUID,
                   minorRadius=a,
                   wallRadius=1.2*a,
                   include=['fluid/runawayRate', 'fluid/gammaDreicer'],
                   output=f'outputs/neglect.h5',
                   save=f'settings/neglect.h5')

    ConfigureDREAM(avalanche=AVALANCHE_FLUID,
                   avaTrapping=AVALANCHE_TRAPPING_INCLUDE,
                   minorRadius=a,
                   wallRadius=1.2*a,
                   include=['fluid/GammaAva', 'fluid/runawayRate', 'fluid/gammaDreicer'],
                   output=f'outputs/include.h5',
                   save=f'settings/include.h5')
