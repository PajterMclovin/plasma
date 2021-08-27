#!/bin/python3
"""
Created by Hannes Bergström 26/8/2021.

Visualizes DREAM output data for with respect to electric field strength.
"""
# do.grid.effectivePassingFraction

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import sys, os, glob

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
   	
      if not geometry or geometry == 'toroidal':
         ax.plot(runawayRate, '-', label = f'{do.eqsys.E_field[0,0]}')
      elif geometry == 'cylindrical':
         ax.plot(runawayRate, 'k--')
      else:
         raise Exception('\nInvalid geometry\n')

   return ax



if __name__ == '__main__':

    fig, ax = plt.subplots()
    
    cylFiles = glob.glob(outputDir+'/*cyl*.h5')
    torFiles = glob.glob(outputDir+'/*tor*.h5')
    
    if cylFiles and torFiles:
       print('\nCylindrical and toroidal simulation data found, ploting both.\n')
       
       plotRadialProfile(ax, cylFiles, geometry = 'cylindrical')
       plt.gca().set_prop_cycle(None)
       plotRadialProfile(ax, torFiles, geometry = 'toroidal')
       
       if len(torFiles)>1:
          ax.legend(title = 'electric field [V/m]')
          
       # plots the effective passing fraction
       fp = torFiles[1]
       do = DREAMOutput(os.path.join(outputDir, fp))
       effPassing = do.grid.effectivePassingFraction
       ax.plot(effPassing, 'k:')
       
       custom_lines = [Line2D([0], [0], color = 'k', ls = '-'), 
       Line2D([0], [0], color= 'k', ls = '--'), 
       Line2D([0], [0], color= 'k', ls = ':')]
       
       ax2 = ax.twinx()
       ax2.legend(custom_lines,['toroidal geometry', 'cylindric geometry', 'effective passing fraction'], loc = 7)
       
    elif cylFiles:
       print('\nCylindrical measurement data found.\n')
       plotElectricScan(ax, cylFiles)
    elif torFiles:
       print('\nToroidal measurement data found.\n')
       plotElectricScan(ax, torFiles)
    else:
       raise Exception('\nNo measurement data found.\n')
    
    
    # plot settings
    plt.ylabel('relative runaway rate')
    plt.xlabel('radial grid point')
    plt.show()
