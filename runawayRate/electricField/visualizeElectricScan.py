#!/bin/python3
"""
Created by Hannes Bergström 25/8/2021.

Visualizes DREAM output data for with respect to electric field strength.
"""


import matplotlib.pyplot as plt
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

def plotElectricScan(ax, files):
   E = np.zeros(len(files))
   runawayRate = np.zeros(len(files))
        
   for i in range(len(files)):
      do = DREAMOutput(os.path.join(outputDir, files[i]))
      E[i] = do.eqsys.E_field[0,0]
      runawayRate[i] = do.other.fluid.runawayRate.data[-1,0]
   
   sorted_indices =  E.argsort()   
   ax.plot(E[sorted_indices], runawayRate[sorted_indices])

   return ax



if __name__ == '__main__':

    fig, ax = plt.subplots()
    
    cylFiles = glob.glob(outputDir+'/*cyl*.h5')
    torFiles = glob.glob(outputDir+'/*tor*.h5')
    
    if cylFiles and torFiles:
       print('\nCylindrical and toroidal simulation data found, ploting both.\n')
       plotElectricScan(ax, cylFiles)
       plotElectricScan(ax, torFiles)
       ax.legend(['Cylindrical', 'Toroidal'], title = 'Geometry')
    elif cylFiles:
       print('\nCylindrical measurement data found.\n')
       plotElectricScan(ax, cylFiles)
    elif torFiles:
       print('\nToroidal measurement data found.\n')
       plotElectricScan(ax, torFiles)
    else:
       raise Exception('\nNo measurement data found.\n')
    
    # plot settings
    plt.ylabel(r'runaway rate [$s^{-1}m^{-3}$]')
    plt.xlabel('electric field [V/m]')
    plt.show()
