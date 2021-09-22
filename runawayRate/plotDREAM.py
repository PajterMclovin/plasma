#!/bin/python3
"""
Created by Peter Halldestam 7/9/21.
"""
import sys, os
import numpy as np
import matplotlib.pyplot as plt

dir = os.path.dirname(os.path.realpath(__file__))

# Parameter imports
sys.path.append(os.path.join(dir, '..'))
import parameters as p

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput

# set font sizes
SMALL_SIZE = 14
MEDIUM_SIZE = 16
# BIGGER_SIZE = 18
plt.rc('font', size=SMALL_SIZE)          # default
plt.rc('axes', titlesize=SMALL_SIZE)     # axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # x tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # y tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend

# figure size (import this)
FIGSIZE = (10, 5)


def plotRunawayRateTime(do, ax=None, label=None, normalize=False, show=False, verbose=False):
    """
    Plot runaway rate vs. time to check convergence. Returns Axes object.

    DREAM.DREAMOutput do :      DREAM settings object.
    matplotlib.axes.Axes ax :   Axes object used for plotting.
    str label :                 Legend label.
    bool normalize :            Normalize such that the first element of
                                runawayRate is equal to unity.
    bool show :                 Show figure.
    bool verbose :              Show information.
    """
    if verbose:
        print(plotRunawayRate.__doc__)

    try:
        runawayRate = do.other.fluid.runawayRate.data[:,0]
        time = do.other.fluid.runawayRate.time

    except AttributeError as err:
        raise Exception('Output does not include needed data.') from err

    if normalize:
        runawayRate /= runawayRate[0]

    if ax is None:
        ax = plt.axes()

    ax.semilogy(time, runawayRate, label=label)

    if show:
        plt.show()

    return ax


def plotRunawayRateMinorRadius(do, ax=None, label=None, normalize=False, show=False, verbose=False):
    """
    Plot runaway rate vs. the minor radius of the analytical toroidal magnetic
    field to check convergence. Returns Axes object.

    DREAM.DREAMOutput do :      DREAM settings object.
    matplotlib.axes.Axes ax :   Axes object used for plotting.
    str label :                 Legend label.
    bool normalize :            Normalize such that the first element of
                                runawayRate is equal to unity.
    bool show :                 Show figure.
    bool verbose :              Show information.
    """
    if verbose:
        print(plotRunawayRate.__doc__)

    try:
        runawayRate = do.other.fluid.runawayRate.data[-1,:] # at final time step
        minorRadius = do.grid.r

    except AttributeError as err:
        raise Exception(f'Output does not include needed data.') from err

    if normalize:
        runawayRate /= runawayRate[0]

    if ax is None:
        ax = plt.axes()

    ax.plot(minorRadius, runawayRate, label=label)

    if show:
        plt.show()

    return ax


def plotFluxSurface(kappa=None, delta=None, Delta=None, nNodes=100,
                    ax=None, label=None, show=False, verbose=False):
    """
    Plot magnetic flux surface defined by the three shaping parameters kappa,
    delta, and Delta in DREAM's analytical toroidal magnetic field model.
    Returns Axes object.

    float kappa :               Elongation paramater
    float delta :               Triangularity paramater
    float Delta :               Shafranov shift paramater
    int nNodes :                No. nodes to plot the closed curve (xz-plane) with.
    matplotlib.axes.Axes ax :   Axes object used for plotting.
    str label :                 Legend label.
    bool show :                 Show figure.
    bool verbose :              Show information.
    """
    if verbose:
        print(plotFluxSurface.__doc__)
        if all(x is None for x in [kappa, delta, Delta]):
            print('\nPlotting flux surface using default shaping paramaters.')

    kappa = p.MAX_ELONGATION if kappa is None else kappa
    delta = p.MAX_TRIANGULARITY if delta is None else delta
    Delta = p.MAX_SHAFRANOV_SHIFT if Delta is None else Delta

    theta = np.linspace(0, 2*np.pi, nNodes) # poloidal angles
    x = p.MAJOR_RADIUS + Delta + p.MINOR_RADIUS * np.cos(theta + delta * np.sin(theta))
    z = p.MINOR_RADIUS * kappa * np.sin(theta)

    if ax is None:
        ax = plt.axes()

    ax.plot(x, z, label=label)

    if show:
        plt.show()

    return ax

def plotEffectivePassingFractionMinorRadius(do, ax=None, label=None, show=False,
                                            normalize=False, verbose=False):
    """
    plot
    """
    if verbose:
        print(plotEffectivePassingFractionMinorRadius.__doc__)

    try:
        effectivePassingFraction = do.grid.effectivePassingFraction
        minorRadius = do.grid.r

    except AttributeError as err:
        raise Exception(f'Output does not include needed data.') from err

    if normalize:
        effectivePassingFraction /= effectivePassingFraction[0]

    if ax is None:
        ax = plt.axes()

    ax.plot(minorRadius, effectivePassingFraction, label=label)

    if show:
        plt.show()

    return ax


def testplot(outputDir='outputs/', ax=None, label=None, show=False):

    runawayRateValues = []
    gammaDreicerValues = []
    electricFieldValues = []

    for fp in os.listdir(outputDir):
        if fp.endswith('.h5'):
            do = DREAMOutput(os.path.join(outputDir, fp))
            try:
                print(do.other.fluid.runawayRate.data)
                runawayRateValues.append(do.other.fluid.runawayRate.data[-1,0])
                gammaDreicerValues.append(do.other.fluid.gammaDreicer.data[-1,0])
                electricFieldValues.append(np.mean(do.eqsys.E_field.data))

            except AttributeError as err:
                raise Exception('Output does not include needed data.') from err

    if ax is None:
        ax = plt.axes()

    ax.semilogy(electricFieldValues, runawayRateValues, '.', color='red', label='total runaway rate')
    ax.semilogy(electricFieldValues, gammaDreicerValues, '.', color='blue', label='Dreicer generation')

    if show:
        ax.grid(True, which='both')
        ax.minorticks_on()
        ax.legend(loc='lower right')
        ax.set_xlabel(r'electric field $E$ [V m$^{-1}$]')
        ax.set_ylabel(r'Runaway generation [s$^{-1}$ m$^{-3}$]')
        plt.show()

    return ax


if __name__ == '__main__':
    plotFluxSurface(show=True, verbose=(len(sys.argv)==2))
