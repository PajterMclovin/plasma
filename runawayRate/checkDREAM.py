#!/bin/python3
"""
Created by Peter Halldestam 23/8/2021.


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

        Hannes du kirrar denna tack!

    """
    runawarRate = do.other.fluid.runawayRate.data

    converged = False
    if converged:
        msg = "holy shit!"
        if interupt:
            raise Exception(msg)
        else:
            warnings.warn(msg)



if __name__ == '__main__':

    if not len(sys.argv) == 2:
        raise Exception('Must include one argument being the DREAM output file.')

    do = DREAMOutput(sys.argv[1])
    checkElectronDensityRatio(do, interupt=True)
    # checkRunawayRateConvergence(do, interupt=True)
