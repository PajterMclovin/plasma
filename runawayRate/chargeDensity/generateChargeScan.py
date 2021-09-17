#!/usr/bin/python3
"""
Created by Hannes Bergström 8/9/21.

Generates DREAM settings files for a range of elongation maxima (geometric
parameter). Add any single command line argument when running this script to
visualize the magnetic field.
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
from parameters import MAX_ELONGATION

# helper function import
sys.path.append(os.path.join(dir, '../'))
from configureDREAM import ConfigureDREAM

# Scan parameters
scanValues = [('D', 1), ('He2', 2), ('Li3', 3)]

if __name__ == "__main__":

    for scanValue in scanValues:

        ConfigureDREAM(include=['fluid/runawayRate', 'fluid/gammaDreicer'],
                       ion=scanValue, verbose=(len(sys.argv)==2),
                       output=f'outputs/outputZ{scanValue[1]}.h5',
                       save=f'settings/settingZ{scanValue[1]}.h5')
