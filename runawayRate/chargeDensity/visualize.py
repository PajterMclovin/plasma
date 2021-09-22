#!/usr/bin/python3
"""
Created by Hannes Bergström 8/9/2021,

Visualizes the cylindrical distribution and radial profile with 
respect to ion charge for one or more DREAM output files.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os, glob
import time
from matplotlib.colors import Normalize

dir = os.path.dirname(os.path.realpath(__file__))

# plot helper function import
sys.path.append(os.path.join(dir, '../'))
from plotDREAM import plotRunawayRateMinorRadius
from plotDREAM import plotFluxSurface
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Settings object import
sys.path.append(os.path.join(dir, '../../'))
from parameters import DREAM_PATH
sys.path.append(DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')


# visualize specified output
if len(sys.argv) == 2:
    fig, (ax1, ax2) = plt.subplots(1,2)

    do = DREAMOutput(sys.argv[1])
    ax1 = plotRunawayRateMinorRadius(do, ax=ax1)
    
    norm = do.eqsys.f_hot[-1, -1, -1, -3]
    do.eqsys.f_hot.plot2D(r = -1, ax = ax2, coordinates = 'cylindrical', 
                          levels = np.linspace(-5, 5, 40) + np.log10(norm), extend = 'min')

# visualize all outputs
elif len(sys.argv) == 1:
    files = sorted(glob.glob(outputDir+'/*.h5'))

    fig1, ax1 = plt.subplots()
    fig2, ax_list = plt.subplots(1, len(files))
    for ind, fp in enumerate(files):
        outputFile = os.path.join(outputDir, fp)
        do = DREAMOutput(outputFile)
            
        charge = do.eqsys.n_i.ions[0].Z
        label = f'Z = {charge}'
        ax1 = plotRunawayRateMinorRadius(do, ax=ax1, normalize = True, label=label)
        #do.eqsys.f_hot /
        norm = do.eqsys.f_hot[-1, -1, -1, -3]
        do.eqsys.f_hot.plot2D(r = -1, t = 1, ax = ax_list[ind], coordinates = 'cylindrical',
                              levels = np.linspace(-5, 5, 40) + np.log10(norm), extend = 'min')
        ax_list[ind].set_title(f'atomic charge: Z = {charge}')
        
    ax1.legend(title='atomic charge')

else:
    raise ValueError('Expected at most one argument.')

# plot settings
ax1.set_ylabel(r'runaway rate $\gamma$ [m$^{-1}$]')
ax1.set_xlabel(r'minor radius $r$ [m]')

plt.show()

