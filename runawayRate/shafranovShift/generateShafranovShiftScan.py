#!/usr/bin/python3
"""
Created by Peter Halldestam 1/9/21.

Generates DREAM settings files for a range of Shafranov shift maxima (geometric parameter).
Add any single command line argument when running this script to visualize the magnetic
field
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '../..'))
import parameters as p

# helper function import
sys.path.append(os.path.join(dir, '..'))
from configureDREAM import configureEquations

# Settings object import
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMSettings import DREAMSettings

# Scan parameters
nScanValues = 3
scanValues = p.MAX_SHAFRANOV_SHIFT * np.linspace(.5, 10, nScanValues)


def configureGrids(ds, maxShafranovShift=None, verbose=False, visualize=False):
    """
    Configure numerical grids.

    DREAM.DREAMSettings ds :    Settings object to configure.
    float maxShafranovShift :   Maximum Shafranov shift (geometry parameter). (MAX MIN??)
    bool verbose :              Show more information during program if True.
    """


    # set type (2 = Analytic toroidal)
    ds.radialgrid.setType(2)

    # Toroidal field function
    GOverR0 = p.MAGNETIC_FIELD     # = R*Bphi/R0

    # Poloidal flux
    rpsi   = np.linspace(0, p.MINOR_RADIUS, p.N_POLODIAL_FLUX)
    psi = -p.MU_0 * p.PLASMA_CURRENT * (1-(rpsi / p.MINOR_RADIUS)**2) * p.MINOR_RADIUS

    # Set up input radial grids
    rDelta = np.linspace(0, p.MINOR_RADIUS, p.N_SHAFRANOV_SHIFT)
    rdelta = np.linspace(0, p.MINOR_RADIUS, p.N_TRIANGULARITY)
    rkappa = np.linspace(0, p.MINOR_RADIUS, p.N_ELONGATION)

    # Set shaping parameters
    delta = np.linspace(0, p.MAX_TRIANGULARITY, p.N_TRIANGULARITY)
    kappa = np.linspace(0, p.MAX_ELONGATION, p.N_ELONGATION)

    if maxShafranovShift is None:
        maxShafranovShift = p.MAX_SHAFRANOV_SHIFT
    elif maxShafranovShift < 0:
        pass

    Delta = np.linspace(0, maxShafranovShift, p.N_SHAFRANOV_SHIFT)

    # set radial grid shape
    ds.radialgrid.setMajorRadius(p.MAJOR_RADIUS)
    ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0,
                             kappa=kappa, rkappa=rkappa,
                             Delta=Delta, rDelta=rDelta,
                             delta=delta, rdelta=rdelta)

    # automatically adjust xi-grid
    ds.hottailgrid.setTrappedPassingBoundaryLayerGrid(dxiMax=p.MAX_PITCH_STEP)

    # general radial grid settings
    ds.radialgrid.setWallRadius(p.WALL_RADIUS)
    ds.radialgrid.setMinorRadius(p.MINOR_RADIUS)
    ds.radialgrid.setNr(p.N_RADIUS)

    if visualize:
        ds.radialgrid.visualize(show=True)

    # hot-tail grid settings
    ds.hottailgrid.setNxi(p.N_PITCH)
    ds.hottailgrid.setNp(p.N_MOMENTUM)
    ds.hottailgrid.setPmax(p.MAX_MOMENTUM)

    # time grid settings
    ds.timestep.setTmax(p.MAX_TIME)
    ds.timestep.setNt(p.N_TIME)

    # Disable runaway grid
    ds.runawaygrid.setEnabled(False)



if __name__ == "__main__":

    for maxShafranovShift in scanValues:

    	# Generate DREAM setting with torodial geometry with varying maximum elongation
        ds = DREAMSettings()
        configureGrids(ds, maxShafranovShift=maxShafranovShift, visualize=(len(sys.argv)==2))
        configureEquations(ds)
        ds.output.setFilename(f'outputs/output{maxShafranovShift}.h5')
        ds.other.include('fluid/runawayRate')
        ds.save(f'dream_settings/settings{maxShafranovShift}.h5')
