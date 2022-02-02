#!/usr/bin/python3
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
sys.path.append(os.path.join(dir, '../../..'))
from plotDREAM import FIGSIZE
from plotDREAM import plotRunawayRateMinorRadius

# Parameters import
sys.path.append(os.path.join(dir, '../../../..'))
import parameters as p

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

sys.path.append(os.path.join(dir, 'outputs'))
outputDir = os.path.join(dir, 'outputs')



if __name__ == '__main__':

    fig, ax = plt.subplots()

    # analytic formula from E Nilsson et al (not finished)
    """
    n_e = p.ELECTRON_DENSITY
    c = 299792458
    q = 1.6e-19
    lnC = 4
    epsilon_0 = 8.85e-12
    m_0 = 9.1e-31

    E_c = n_e * q**3 * lnC / (4*np.pi * epsilon_0**2 * m_0 * c**2)
    E_field = 40*E_c

    def ava_fit(epsilon):
        theta = theta_bound(epsilon)


    def theta_bound(epsilon):
        return 2*np.arctan(np.sqrt(4*epsilon*E_field/E_c-(1-epsilon))/np.sqrt(1-epsilon))

    eps_plot = np.linspace(0, 1)
    d_fit = ava_fit(eps_plot)
    eps_plot = eps_plot[d_fit >=0]
    d_fit = d_fit[d_fit >= 0]
    ax.plot(eps_plot, d_fit, alpha=0.8, label = r'E Nilsson et al')
    """

    # help function that extracts the final growth rate at different positions
    def extract_Gamma(runawayRate, n_re):
        return runawayRate[-1,:]/n_re[-1,:]

    # selects files
    if len(sys.argv) == 1:
       fp_cyl = glob.glob(outputDir+'/*cyl.h5')[0]
       fp_tor = glob.glob(outputDir+'/*tor.h5')[0]
    else:
        raise ValueError('No arguments expected.')

    # checks if data for both geometries could be found
    if fp_cyl and fp_tor:

        # loads data and determines growth rate
        do_cyl = DREAMOutput(fp_cyl)
        do_tor = DREAMOutput(fp_tor)

        GammaAvaCyl = extract_Gamma(do_cyl.other.fluid.runawayRate.data, do_cyl.eqsys.n_re.data)
        GammaAvaTor = extract_Gamma(do_tor.other.fluid.runawayRate.data, do_tor.eqsys.n_re.data)

        # plots the relative growth rate as a function on epsilon
        frac = np.concatenate((np.array([1]), GammaAvaTor/GammaAvaCyl))
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
    plt.xlabel(r'$\epsilon$')
    plt.ylabel(r'$\Gamma_{A} / \Gamma_{A, cyl}$')
    #plt.ylim((0, 1))
    #plt.xlim((0, 1))
    plt.grid()
    #plt.legend()
    #plt.savefig('avalanche_plot.png')
    plt.show()
