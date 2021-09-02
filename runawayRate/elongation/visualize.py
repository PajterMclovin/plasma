#!/bin/python3
"""
Created by Peter Halldestam 1/9/2021.

Visualizes DREAM output data for a range of maximum elongation.
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
from DREAM.DREAMSettings import DREAMSettings

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')

def plotRunawayRate(do, ax=None, label=None):
    """
    Plot runaway rate vs. minor radii.

    DREAM.DREAMOutput do :      DREAM settings object.
    matplotlib.axes.Axes ax :   Axes object used for plotting.
    str label :                 Legend label.
    """
    if ax is None:
        ax = plt.axes()

    # load relevant DREAM output quantities
    try:
        minorRadius = do.grid.r
        runawayRate = do.other.fluid.runawayRate.data[0,:]
    except AttributeError as err:
        raise Exception(f'Output file {fp} does not include .') from err

    # plot runaway rate vs time
    print(len(minorRadius))
    ax.plot(minorRadius, runawayRate, label=label)
    return ax

if __name__ == '__main__':

    fig, ax = plt.subplots()

    # visualize specified output
    if len(sys.argv) == 2:
        ax = plotRunawayRate(sys.argv[1])

    # visualize all outputs
    elif len(sys.argv) == 1:
        for fp in os.listdir(outputDir):
            if fp.endswith(".h5"):
                print('he')
                outputFile = os.path.join(outputDir, fp)
                do = DREAMOutput(outputFile)
                ds = DREAMSettings().fromOutput(outputFile)
                # temperature = np.mean(do.eqsys.T_cold.data)
                print(fp)
                max_elongation = fp[len('outputs'):]
                ax = plotRunawayRate(do, ax=ax, label=max_elongation)

    else:
        raise ValueError('Expected at most one argument.')

    # plot settings
    plt.legend(title='electric field [V/m]')
    plt.ylabel(r'runaway rate [$s^{-1}m^{-3}$]')
    # plt.xlabel(r'time [$s$]')
    plt.show()
