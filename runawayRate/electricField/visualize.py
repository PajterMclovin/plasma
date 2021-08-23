#!/bin/python3
"""
Created by Peter Halldestam 19/8/21.
Modified by Hannes Bergström.

Visualizes DREAM output data for a range of electric fields.
"""


import matplotlib.pyplot as plt
import numpy as np
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
import parameters as p

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

# helper function import
sys.path.append(os.path.join(dir, '..'))
from configureDREAM import plotRunawayRate

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')

if __name__ == '__main__':

    fig, ax = plt.subplots()
    
    # visualize specified output
    if len(sys.argv) == 2:
        ax = plotRunawayRate(sys.argv[1])

    # visualize all outputs
    elif len(sys.argv) == 1:
        for fp in os.listdir(outputDir):
            if fp.endswith(".h5"):
                do = DREAMOutput(os.path.join(outputDir, fp))
                temperature = np.mean(do.eqsys.T_cold.data)
                ax = plotRunawayRate(do, ax=ax, label=do.eqsys.E_field[0,0])

    else:
        raise ValueError('Expected at most one argument.')

    # plot settings
    plt.legend(title='electric field [V/m]')
    plt.ylabel(r'runaway rate [$s^{-1}m^{-3}$]')
    plt.xlabel(r'time [$s$]')
    plt.show()
