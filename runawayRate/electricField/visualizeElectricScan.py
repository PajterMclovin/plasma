#!/bin/python3
"""
Created by Hannes Bergström 25/8/2021.

Visualizes DREAM output data for with respect to electric field strength.
"""


import matplotlib.pyplot as plt
import numpy as np
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
import parameters as p

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')

if __name__ == '__main__':

    fig, ax = plt.subplots()

    if len(sys.argv) == 1:
        dirList = [fp for fp in os.listdir(outputDir) if fp.endswith(".h5")]
        dirList.sort()
        E = np.zeros(len(dirList))
        runawayRate = np.zeros(len(dirList))
        
        for i in range(len(dirList)):
            fp = dirList[i]
            do = DREAMOutput(os.path.join(outputDir, fp))
            E[i] = do.eqsys.E_field[0,0]
            runawayRate[i] = do.other.fluid.runawayRate.data[-1,17]
        
        sorted_indices =  E.argsort()   
        ax.plot(E[sorted_indices], runawayRate[sorted_indices])
                
    else:
        raise ValueError('Did not expect any arguments.')

    # plot settings
    plt.ylabel(r'runaway rate [$s^{-1}m^{-3}$]')
    plt.xlabel('electric field [V/m]')
    plt.show()
