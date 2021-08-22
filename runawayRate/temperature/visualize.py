#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))

# helper function import
sys.path.append(os.path.join(dir, '..'))
from configureDREAM import plotRunawayRate

outputDir = sys.path.append(os.path.join(dir, 'outputs'))


if __name__ == '__main__':

    fig, ax = plt.subplots()

    # visualize specified output
    if len(sys.argv) == 2:
        ax = plotRunawayRate(sys.argv[1])

    # visualize all outputs
    elif len(sys.argv) == 1:
        for fp in os.listdir(outputDir):
            if fp.endswith(".h5"):
                print(fp)
                do = DREAMOutput(os.path.join(outputDir, fp))
                temperature = np.mean(do.eqsys.T_cold.data)
                ax = plotRunawayRate(do, ax=ax, label=temperature)

    else:
        raise ValueError('Expected at most one argument.')

    # plot settings
    plt.legend(title='temperature [eV]')
    plt.ylabel(r'runaway rate [$s^{-1}m^{-3}$]')
    plt.xlabel(r'time [$s$]')
    plt.show()
