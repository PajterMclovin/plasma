#!/bin/python3
"""
Created by Hannes Bergström 26/8/2021.

Visualizes DREAM output data for with respect to electric field strength.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os, glob
from matplotlib.lines import Line2D

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
import parameters as p

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')

def plotRadialProfile(ax, files, geometry = None):
   
   
   for fp in files:
      do = DREAMOutput(os.path.join(outputDir, fp))
      runawayRate = do.other.fluid.runawayRate.data[-1,:] / do.other.fluid.runawayRate.data[-1,0] 
      minorRC = do.grid.r
   	
      if not geometry or geometry == 'toroidal':
         ax.plot(minorRC, runawayRate, '-', label = f'{do.eqsys.E_field[0,0]}')
      elif geometry == 'cylindrical':
         ax.plot(minorRC, runawayRate, 'k--')
      else:
         raise Exception('\nInvalid geometry\n')

   return ax



if __name__ == '__main__':

    fig, ax = plt.subplots()
    
    # uses standard output file
    if len(sys.argv) == 1:
       cylFiles = sorted(glob.glob(outputDir+'/*cyl*.h5'))
       torFiles = sorted(glob.glob(outputDir+'/*tor*.h5'))
       
    # uses specified output file
    elif len(sys.argv) == 2:
       specDir = os.path.join(dir, sys.argv[1])
       cylFiles = sorted(glob.glob(specDir+'/*cyl*.h5'))
       torFiles = sorted(glob.glob(specDir+'/*tor*.h5'))
    
    else:
        raise ValueError('Expected at most one argument.')
    
    # considers different cases of simulated geometries
    if cylFiles and torFiles:
       print('\nCylindrical and toroidal simulation data found, ploting both.\n')
       
       plotRadialProfile(ax, cylFiles, geometry = 'cylindrical')
       plotRadialProfile(ax, torFiles, geometry = 'toroidal')
       
       if len(torFiles)>1:
          ax.legend(title = 'electric field [V/m]')
          
       # plots the effective passing fraction
       fp = torFiles[0]
       do = DREAMOutput(os.path.join(outputDir, fp))
       effPassing = do.grid.effectivePassingFraction
       minorRC = do.grid.r
       ax.plot(minorRC, effPassing, 'k:')
       
       # adds second legend
       custom_lines = [Line2D([0], [0], color = 'k', ls = '-'), 
       Line2D([0], [0], color= 'k', ls = '--'), 
       Line2D([0], [0], color= 'k', ls = ':')]
       ax2 = ax.twinx()
       ax2.legend(custom_lines,['toroidal geometry', 'cylindric geometry', 'effective passing fraction'], loc = 7)
       
    elif cylFiles:
       print('\nCylindrical simulation data found.\n')
       plotElectricScan(ax, cylFiles)
       
    elif torFiles:
       print('\nToroidal simulation data found.\n')
       plotElectricScan(ax, torFiles)
       
    else:
       raise Exception('\nNo simulation data found.\n')
    
    
    # plot settings
    ax.set_ylabel('relative runaway rate')
    ax.set_xlabel('minor radial coordinate [m]')
    plt.show()
