#!/bin/python3
"""
Created by Peter Halldestam 1/9/21.
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
nScanValues = 6
scanValues = p.MAX_ELONGATION * np.linspace(.1, 10, nScanValues)


def configureGrids(ds, max_elongation=None, verbose=False, visualize=False):
    """
    Configure numerical grids.

    DREAM.DREAMSettings ds :    Settings object to configure.
    float max_elongation :      Maximum elongation (geometry parameter). (MAX MIN??)
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
    Delta = np.linspace(0, p.MAX_SHAFRANOV_SHIFT, p.N_SHAFRANOV_SHIFT)
    delta = np.linspace(0, p.MAX_TRIANGULARITY, p.N_TRIANGULARITY)

    if max_elongation is None:
        max_elongation = p.MAX_ELONGATION
    elif max_elongation < 0:
        pass

    kappa = np.linspace(0, max_elongation, p.N_ELONGATION)

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

    for max_elongation in scanValues:

        # Cylindrical geometry
        ds = DREAMSettings()
        configureGrids(ds, max_elongation=max_elongation, visualize=True)
        configureEquations(ds)
        ds.output.setFilename(f'outputs/output{max_elongation}.h5')
        ds.other.include('fluid/runawayRate')
        ds.save(f'dream_settings/settings{max_elongation}.h5')

        # Toroidal geometry
        # ds2 = DREAMSettings()
        # c.configureGrids(ds2, geometry=c.TOROIDAL)
        # c.configureEquations(ds2, electricField=electricField)
        # ds2.output.setFilename(F'outputs/output_tor_E={electricField:2.3}.h5')
        # ds2.other.include('fluid/runawayRate')
        # ds2.save(f'dream_settings/settings_tor_E={electricField:2.3}.h5')
