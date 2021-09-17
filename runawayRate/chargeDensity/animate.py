#!/usr/bin/python3
"""
Created by Hannes Bergström 17/9/2021,

Animates the cylindrical momentum distribution with respect to
ion charge for one or more DREAM output files.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os, glob
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
    fig, ax = plt.subplots()
    do = DREAMOutput(sys.argv[1])

    dos = [do]
    ax_list = [ax]

# visualize all outputs
elif len(sys.argv) == 1:  
    files = sorted(glob.glob(outputDir+'/*.h5'))
    fig, ax_list = plt.subplots(1, len(files))
    
    dos = []
    for ind, fp in enumerate(files):
        outputFile = os.path.join(outputDir, fp)
        dos.append(DREAMOutput(outputFile))
        
        charge = dos[ind].eqsys.n_i.ions[0].Z
        ax_list[ind].set_title(f'atomic charge: Z = {charge}')
       
else:
    raise ValueError('Expected at most one argument.')
        
    
# run animation
while plt.fignum_exists(fig.number):
    for t in range(1,len(dos[0].grid.t)):
        for ind, do in enumerate(dos):
            do.eqsys.f_hot.plot2D(r = -1, t = t, ax = ax_list[ind], coordinates = 'cylindrical', vmin = -15, vmax = 25, levels = 10)
        try:
            plt.pause(1)
        except:
            print('program closed')
            break
            





