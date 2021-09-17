#!/bin/python3
"""
Created by Peter Halldestam 19/8/21,
modified by Peter Halldestam 8/9/21.

Generates DREAM settings files for a range of electric fields.
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
from parameters import ELECTRIC_FIELD

# Baseline DREAM settings import
sys.path.append(os.path.join(dir, '..'))
from configureDREAM import ConfigureDREAM
from configureDREAM import CYLINDRICAL

# Scan parameters
nScanValues = 10
scanValues = ELECTRIC_FIELD * np.linspace(.5, 3, nScanValues)


if __name__ == "__main__":

    for scanValue in scanValues:

        ConfigureDREAM(include=['fluid/runawayRate', 'fluid/gammaDreicer'],
                       geometry=CYLINDRICAL,
                       electricField=scanValue,
                       output=f'outputs/output{scanValue}.h5',
                       save=f'settings/setting{scanValue}.h5',
                       verbose=(len(sys.argv)==2))
