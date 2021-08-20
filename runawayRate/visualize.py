#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append('../../../../DREAM/py')  # /path/to/DREAM/py

from DREAM import *
from DREAM.DREAMOutput import DREAMOutput

DREAM_OUTPUTS_DIR = './outputs/'

# do = DREAMOutput('outputs/demo_output.h5')
# time = do.other.fluid.runawayRate.time

def plotRunawayRate(fp, ax=None, label=None):
    """
    Plot runaway rate vs. time to check convergence.

    :param str fp:                  Output file path.
    :param matplotlib.axes.Axes ax: Axes object used for plotting.
    """
    if ax is None:
        ax = plt.axes()

    # load relevant DREAM output quantities
    do = DREAMOutput(fp)
    try:
        time = do.other.fluid.runawayRate.time
        runawayRate = do.other.fluid.runawayRate.data[:,0]
    except AttributeError as err:
        raise Exception(f'Output file {fp} does not include .') from err

    if label is None:
        label = f'{np.mean(do.eqsys.E_field.data):2.3}'

    # plot runaway rate vs time
    ax.semilogy(time, runawayRate, label=label)
    return ax



if __name__ == '__main__':

    fig, ax = plt.subplots()

    # visualize one specified output
    if len(sys.argv) == 2:
        ax = plotRunawayRate(sys.argv[1], ax=ax)

    # visualize all outputs
    elif len(sys.argv) == 1:
        for fp in os.listdir(DREAM_OUTPUTS_DIR):
            if fp.endswith(".h5"):

                ax = plotRunawayRate(os.path.join(DREAM_OUTPUTS_DIR, fp), ax=ax)

                continue
            else:
                continue

    else:
        raise ValueError('ERROR: Invalid command line arguments. Expected at most one argument.')

    # plot settings
    plt.legend(title='electric field [V/m]')
    plt.ylabel(r'runaway rate [$s^{-1}m^{-3}$]')
    plt.xlabel(r'time [$s$]')
    plt.show()
