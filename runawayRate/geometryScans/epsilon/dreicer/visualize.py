#!/bin/python3
"""
Created by Hannes Bergström 25/11/2021.

Visualizes DREAM runaway rate output as a function of epsilon = "minor radial coordinate" / "major radius".
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os, glob
from matplotlib.lines import Line2D

dir = os.path.dirname(os.path.realpath(__file__))

# plot helper function import
sys.path.append(os.path.join(dir, '../..'))
from plotDREAM import FIGSIZE
from plotDREAM import plotRunawayRateMinorRadius

# Parameters import
sys.path.append(os.path.join(dir, '../../..'))
import parameters as p

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')



if __name__ == '__main__':

    def dreicer_fit(epsilon):
        return 1 - 1.2*np.sqrt(2*epsilon / (1 + epsilon))

    fig, ax = plt.subplots()
    
    eps_plot = np.linspace(0, 1)
    d_fit = dreicer_fit(eps_plot)
    eps_plot = eps_plot[d_fit >=0]
    d_fit = d_fit[d_fit >= 0]
        
    ax.plot(eps_plot, d_fit, alpha=0.8, label = r'E Nilsson et al')

    # uses standard output file
    if len(sys.argv) == 1:
       fp_cyl = glob.glob(outputDir+'/*cyl.h5')[0]
       fp_tor = glob.glob(outputDir+'/*tor.h5')[0]
    
    else:
        raise ValueError('Expected at most one argument.')
    
    # considers different cases of simulated geometries
    if fp_cyl and fp_tor:
        do_cyl = DREAMOutput(fp_cyl)
        do_tor = DREAMOutput(fp_tor)
        
        gammaDreicerCyl = do_cyl.other.fluid.runawayRate.data[-1,:]
        gammaDreicerTor = do_tor.other.fluid.runawayRate.data[-1,:]
        frac = np.concatenate((np.array([1]), gammaDreicerTor/gammaDreicerCyl))
        minorRC = np.concatenate((np.array([0]), do_tor.grid.r))
        epsilon = minorRC / p.MAJOR_RADIUS
        
        
        ax.scatter(epsilon, frac, facecolors='none', edgecolors='k', clip_on=False, label = 'DREAM')
        
        
    elif fp_cyl:
       raise Exception('\nNo toroidal simulation data found.\n')
       
    elif fp_tor:
       raise Exception('\nNo cylindrical simulation data found.\n')
    
    else:
       raise Exception('\nNo simulation data found.\n')
    
    
    # plot settings
    #ax.legend(title = 'quantity')
    plt.xlabel(r'$\epsilon$')
    plt.ylabel(r'$\gamma_{D} / \gamma_{D, cyl}$')
    plt.ylim((0, 1))
    plt.xlim((0, 1))
    plt.grid()
    plt.legend()
    plt.savefig('dreicer_plot.png')
    plt.show()
    
