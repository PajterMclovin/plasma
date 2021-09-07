#!/usr/bin/python3
"""
Created by Peter Halldestam 1/9/21,
modified by peter Halldestam 7/9/21.

Generates DREAM settings files for a range of elongation maxima (geometric
parameter). Add any single command line argument when running this script to
visualize the magnetic field.
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../../..'))
from parameters import MAX_ELONGATION

# helper function import
sys.path.append(os.path.join(dir, '../..'))
from configureDREAM import ConfigureDREAM

# Scan parameters
nScanValues = 3
scanValues = MAX_ELONGATION * np.linspace(.5, 2, nScanValues)

if __name__ == "__main__":

    for scanValue in scanValues:

        ConfigureDREAM(include=['fluid/runawayRate', 'fluid/gammaDreicer'],
                       maxElongation=scanValue, verbose=(len(sys.argv)==2),
                       output=f'outputs/output{scanValue}.h5',
                       save=f'settings/setting{scanValue}.h5')
