#!/bin/python3
"""
Created by Peter Halldestam 19/8/21.

Generates DREAM settings files for a range of electric fields.
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
nScanValues = 2
scanValues = p.ELECTRIC_FIELD * np.linspace(1e-1, 1, nScanValues)


if __name__ == "__main__":

    for electricField in scanValues:

        # Cylindrical geometry
        ds1 = DREAMSettings()
        c.configureGrids(ds1, geometry=c.CYLINDRICAL)
        c.configureEquations(ds1, electricField=electricField)
        ds1.output.setFilename(F'outputs/output_cyl_E={electricField:2.3}.h5')
        ds1.other.include('fluid/runawayRate')
        ds1.save(f'dream_settings/settings_cyl_E={electricField:2.3}.h5')

        # Toroidal geometry
        # ds2 = DREAMSettings()
        # c.configureGrids(ds2, geometry=c.TOROIDAL)
        # c.configureEquations(ds2, electricField=electricField)
        # ds2.output.setFilename(F'outputs/output_tor_E={electricField:2.3}.h5')
        # ds2.other.include('fluid/runawayRate')
        # ds2.save(f'dream_settings/settings_tor_E={electricField:2.3}.h5')
