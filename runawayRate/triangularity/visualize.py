#!/usr/bin/python3
"""
Created by Peter Halldestam 1/9/2021.

Visualizes DREAM output data for a range of maximum triangularity.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))

# plot helper function import
sys.path.append(os.path.join(dir, '..'))
from configureDREAM import plotRunawayRate

# Settings object import
sys.path.append(os.path.join(dir, '../..'))
from parameters import DREAM_PATH
sys.path.append(DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')


fig, ax = plt.subplots()

# visualize specified output
if len(sys.argv) == 2:
    ax = plotRunawayRate(sys.argv[1])

# visualize all outputs
elif len(sys.argv) == 1:
    for fp in os.listdir(outputDir):
        if fp.endswith(".h5"):
            outputFile = os.path.join(outputDir, fp)
            do = DREAMOutput(outputFile)
            maxTriangularity = fp[len('output'):-3]
            ax = plotRunawayRate(do, ax=ax, label=maxTriangularity, normalize=True)

else:
    raise ValueError('Expected at most one argument.')

# plot settings
plt.legend(title='max triangularity')
plt.ylabel(r'runaway rate')
plt.xlabel(r'minor radius [m]')
plt.show()
