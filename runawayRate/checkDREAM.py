#!/bin/python3
"""
Created by Peter Halldestam 23/8/2021.
Modified by Hannes Bergström.

This file contains helper functions for quick

"""
import sys, os, warnings
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '..'))
import parameters as p

# Output object imports
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMOutput import DREAMOutput


def checkElectronDensityRatio(do, interupt=False):
    """
    Checks whether given output contains instances where the assumption
    n_re << n_cold or not. It is invalid when the ratio n_re / n_cold is smaller
    that some tolerance TOL_ELECTRON_DENSITY_RATIO (defined in parameters.py).
    If invalid, a warning is shown (or exception if interupt is True).

    DREAM.DREAMOutput do :  DREAM output object.
    bool interupt :         Interupts program by raising an exception rather
                            than only showing a warning.
    """
    n_re = do.eqsys.n_re.data
    n_cold = do.eqsys.n_cold.data
    if np.max(n_re / n_cold) > p.TOL_ELECTRON_DENSITY_RATIO:
        msg = f'\n\nn_re / n_cold > {p.TOL_ELECTRON_DENSITY_RATIO} found in {do.filename}'
        if interupt:
            raise Exception(msg)
        else:
            warnings.warn(msg)


def checkRunawayRateConvergence(do, interupt=False):
    """
    Checks if the runaway rate in the given output has converged with respect to time.
    It is considered to have converged if the relative difference between the runaway rate
    at the last time step and the runaway rate at some percentage of the total simulated time
    is smaller than some tolerance.
    The percentage at which the rates are compared is specified by LIM_RUNAWAY_RATE_CONVERGENCE
    and the tolerance is specified by TOL_RUNAWAY_RATE_CONVERGENCE (defined in parameters.py).
    
    DREAM.DREAMOutput do :  DREAM output object.
    bool interupt :         Interupts program by raising an exception rather
                            than only showing a warning.
    """
    runawayRate = do.other.fluid.runawayRate.data
    sample = int(p.LIM_RUNAWAY_RATE_CONVERGENCE * (runawayRate.shape[0]-1))
    
    converged = False
    if np.max(np.abs(runawayRate[-1] - runawayRate[sample]) / runawayRate[-1]) < p.TOL_RUNAWAY_RATE_CONVERGENCE:
    	converged = True
    
    if not converged:
        msg = f"\n\nTransient convergence of runaway rate not obtained in {do.filename}. Convergence after {p.LIM_RUNAWAY_RATE_CONVERGENCE*100}% is not within {p.TOL_RUNAWAY_RATE_CONVERGENCE}"
        if interupt:
            raise Exception(msg)
        else:
            warnings.warn(msg)



if __name__ == '__main__':

    print(sys.argv[1])
    if not len(sys.argv) == 2:
        print(sys.argv)
        raise Exception('Must include one argument being the DREAM output file.')


    do = DREAMOutput(sys.argv[1])
    checkElectronDensityRatio(do, interupt=True)
    checkRunawayRateConvergence(do, interupt=True)
