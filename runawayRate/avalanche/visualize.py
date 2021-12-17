#!/usr/bin/python3
"""
Created by Peter Halldestam 10/12/2021,
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))

# plot helper function import
sys.path.append(os.path.join(dir, '..'))
from plotDREAM import FIGSIZE
from plotDREAM import plotAvalancheMultiplicationFactor, plotRunawayRateMinorRadius

# Settings object import
sys.path.append(os.path.join(dir, '../..'))
from parameters import DREAM_PATH
sys.path.append(DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')


def getGammaAva(do):
    try:
        gammaDreicer = do.other.fluid.gammaDreicer[-1,:]
        runawayRate = do.other.fluid.runawayRate[-1,:]
        nRe = do.eqsys.n_re[-1,:]
        return (runawayRate - gammaDreicer) / nRe
    except AttributeError as err:
        raise Exception('Output does not include needed data.') from err

# initialize figure and axes
fig, ax = plt.subplots(figsize=FIGSIZE)

# visualize specified output
if len(sys.argv) == 2:
    ax = plotAvalancheMultiplicationFactor(sys.argv[1], ax=ax)

# visualize all outputs
elif len(sys.argv) == 1:

    for fp in os.listdir(outputDir):
        if fp.endswith('baseline.h5'):
            do = DREAMOutput(os.path.join(outputDir, fp))
            GammaAva0 = getGammaAva(do)[0]

    for fp in os.listdir(outputDir):

        # load output and plot
        if fp.endswith('.h5') and not fp.endswith('baseline.h5'):
            do = DREAMOutput(os.path.join(outputDir, fp))
            GammaAva = getGammaAva(do) / GammaAva0
            epsilon = do.grid.r / do.grid.R0
            ax.plot(epsilon, GammaAva, label=fp.split('.')[0])


else:
    raise ValueError('Expected at most one argument.')

# plot settings
plt.legend()
ax.set_ylabel(r'$\bar{\Gamma}$ [s$^{-1}$]')
ax.set_xlabel(r'$\epsilon$')
plt.show()
