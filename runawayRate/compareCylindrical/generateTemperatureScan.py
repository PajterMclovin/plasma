#!/bin/python3
"""
Created by Peter Halldestam 19/8/21.

Generates DREAM settings files for a range of temperatures.
"""
import sys
import numpy as np
import configureDREAM as c

# Settings object import
sys.path.append('../../../../DREAM/py')  # /path/to/DREAM/py
from DREAM.DREAMSettings import DREAMSettings

# Physical parameters import
sys.path.append('../..')
import parameters as p

# Scan parameters
nScanValues = 2
scanValues = p.TEMPERATURE * np.linspace(1e-3, 1e2, nScanValues)

if __name__ == "__main__":

    for temperature in scanValues:

        # Cylindrical geometry
        ds1 = DREAMSettings()
        c.configureGrids(ds1, geometry=c.CYLINDRICAL)
        c.configureEquations(ds1, temperature=temperature)
        ds1.output.setFilename(F'outputs/output_cyl_T={temperature:2.3}.h5')
        ds1.other.include('fluid/runawayRate')
        ds1.save(f'dream_settings/settings_cyl_T={temperature:2.3}.h5')

        # Toroidal geometry
        ds2 = DREAMSettings()
        c.configureGrids(ds2, geometry=c.TOROIDAL)
        c.configureEquations(ds2, temperature=temperature)
        ds2.output.setFilename(F'outputs/output_tor_T={temperature:2.3}.h5')
        ds2.other.include('fluid/runawayRate')
        ds2.save(f'dream_settings/settings_tor_T={temperature:2.3}.h5')
