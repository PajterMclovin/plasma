#!/usr/bin/python3
"""
Created by Peter Halldestam 1/9/2021,
modified by Peter Halldestam 7/9/2021.

Visualizes DREAM output data for a range of maximum Shafranov shifts.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))

# plot helper function import
sys.path.append(os.path.join(dir, '../..'))
from plotDREAM import FIGSIZE
from plotDREAM import plotEffectivePassingFractionMinorRadius
from plotDREAM import plotRunawayRateMinorRadius
from plotDREAM import plotFluxSurface

# Settings object import
sys.path.append(os.path.join(dir, '../../..'))
from parameters import DREAM_PATH
sys.path.append(DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')

# initialize figure and 1x2 axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

# visualize specified output
if len(sys.argv) == 2:
    ax1 = plotRunawayRate(sys.argv[1], ax=ax1)
    ax2 = plotFluxSurface(ax=ax2)

# visualize all outputs
elif len(sys.argv) == 1:

    # sort by increasing Shafranov shift
    for fp in sorted(os.listdir(outputDir), key=lambda x: float(x[len('output'):-3])):

        # load output and plot
        if fp.startswith('output') and fp.endswith('.h5'):
            Delta = float(fp[len('output'):-len('.h5')])    # extract Shafranov shift
            outputFile = os.path.join(outputDir, fp)
            do = DREAMOutput(outputFile)
            ax1 = plotRunawayRateMinorRadius(do, ax=ax1, label=f'{Delta:4.5}')
            # ax1 = plotEffectivePassingFractionMinorRadius(do, ax=ax1, label=f'{Delta:4.5}')
            ax2 = plotFluxSurface(Delta=Delta, ax=ax2, label=f'{Delta:4.5}')

else:
    raise ValueError('Expected at most one argument.')

# plot settings
ax1.legend(title=r'Shafranov shift $\Delta$ [m]')
ax1.set_ylabel(r'runaway rate $\gamma$ [m$^{-1}$]')
ax1.set_xlabel(r'minor radius $r$ [m]')
ax2.set_ylabel(r'height $z$[m]')
ax2.set_xlabel(r'major radius $R$ [m]')
ax2.yaxis.set_label_position('right')
ax2.yaxis.tick_right()
plt.show()
