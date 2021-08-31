#!/bin/python3
"""
Created by Hannes Bergström 26/8/21.


Generates DREAM settings files for one or a couple of electric field strengths.
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
import parameters as p

# Baseline DREAM settings import
sys.path.append(os.path.join(dir, '..'))
import configureDREAM as c

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMSettings import DREAMSettings

# Scan parameters
scanValues = [0.8 * p.ELECTRIC_FIELD, p.ELECTRIC_FIELD, 1.2 * p.ELECTRIC_FIELD]


if __name__ == "__main__":

    for i, electricField in enumerate(scanValues):

        print(i)
        # Cylindrical geometry
        ds1 = DREAMSettings()
        c.configureGrids(ds1, geometry=c.CYLINDRICAL)
        c.configureEquations(ds1, electricField=electricField)
        ds1.output.setFilename(f'outputs/output_cyl{i}.h5')
        ds1.other.include('fluid/runawayRate', 'hottail/Dxx')
        ds1.save(f'dream_settings/settings_cyl{i}.h5')

        # Toroidal geometry
        ds2 = DREAMSettings()
        c.configureGrids(ds2, geometry=c.TOROIDAL)
        c.configureEquations(ds2, electricField=electricField)
        ds2.output.setFilename(f'outputs/output_tor{i}.h5')
        ds2.other.include('fluid/runawayRate', 'hottail/Dxx')
        ds2.save(f'dream_settings/settings_tor{i}.h5')
