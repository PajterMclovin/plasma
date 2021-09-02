#!/bin/python3
"""
Created by Peter Halldestam 19/8/21.
Modified by Hannes Bergström 26/8/21
"""
import sys, os
import numpy as np

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import
sys.path.append(os.path.join(dir, '..'))
import parameters as p

# Settings object imports
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMSettings import DREAMSettings
from DREAM.Settings.Equations import IonSpecies
from DREAM.Settings.Equations import RunawayElectrons
from DREAM.Settings.Equations import DistributionFunction
from DREAM.Settings import Solver


# geometries
CYLINDRICAL = 0
TOROIDAL = 1


## helper functions for configuring DREAM settings

def configureGrids(ds, geometry=CYLINDRICAL, verbose=False):
    """
    Configure numerical grids.

    DREAM.DREAMSettings ds :    Settings object to configure.
    int geometry :              Type of geometry (0=cylindrical, 1=toroidal).
    bool verbose :              Show more information during program if True.
    """

    if geometry == CYLINDRICAL:
        if verbose:
            print('setting up a cylindrical geometry')
	
        # set type (1 = Cylindrical)
        ds.radialgrid.setType(1)
        # set radial grid shape
        
        
        #ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0)
        ds.radialgrid.setB0(p.MAGNETIC_FIELD)

    elif geometry == TOROIDAL:
        if verbose:
            print('setting up a toroidal geometry (ITER tokamak?)')
        
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
        kappa = np.linspace(0, p.MAX_ELONGATION, p.N_ELONGATION)

        # set radial grid shape
        ds.radialgrid.setMajorRadius(p.MAJOR_RADIUS)
        ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0,
                                 kappa=kappa, rkappa=rkappa,
                                 Delta=Delta, rDelta=rDelta,
                                 delta=delta, rdelta=rdelta)

        # automatically adjust xi-grid
        ds.hottailgrid.setTrappedPassingBoundaryLayerGrid(dxiMax=p.MAX_PITCH_STEP)

    else:
        raise ValueError("Invalid geometry input!")

    # general radial grid settings
    ds.radialgrid.setWallRadius(p.WALL_RADIUS)
    ds.radialgrid.setMinorRadius(p.MINOR_RADIUS)
    ds.radialgrid.setNr(p.N_RADIUS)

    # hot-tail grid settings
    ds.hottailgrid.setNxi(p.N_PITCH)
    ds.hottailgrid.setNp(p.N_MOMENTUM)
    ds.hottailgrid.setPmax(p.MAX_MOMENTUM)

    # time grid settings
    ds.timestep.setTmax(p.MAX_TIME)
    ds.timestep.setNt(p.N_TIME)

    # Disable runaway grid
    ds.runawaygrid.setEnabled(False)


def configureEquations(ds, electricField=None, temperature=None, verbose=False):
    """
    Configure equation system.

    DREAMSettings ds :      Settings object to configure.
    float electric_field :  Prescribed electric field strength.
    float temperature :     Prescribed temperature:
    bool verbose :          Show more information during program if True.
    """
    # set electric field
    if electricField is None:
        electricField = p.ELECTRIC_FIELD
    ds.eqsys.E_field.setPrescribedData(electricField)

    # set temperature
    if temperature is None:
        temperature = p.TEMPERATURE
    ds.eqsys.T_cold.setPrescribedData(temperature)

    if verbose:
        print(f'Setting the electric field strength to {electricField:2.3} V/m and temperature to {temperature:2.3} eV.')

    # Set initial hot electron Maxwellian
    ds.eqsys.f_hot.setInitialProfiles(n0=p.ELECTRON_DENSITY, T0=temperature)

    # Set ions
    ds.eqsys.n_i.addIon(name='D', Z=1, iontype=IonSpecies.IONS_PRESCRIBED_FULLY_IONIZED, n=p.ELECTRON_DENSITY)

    # Disable avalanche generation
    ds.eqsys.n_re.setAvalanche(avalanche=RunawayElectrons.AVALANCHE_MODE_NEGLECT)

    # Set boundary condition type at pMax
    ds.eqsys.f_hot.setBoundaryCondition(DistributionFunction.BC_F_0) # F=0 outside the boundary
    ds.eqsys.f_hot.setSynchrotronMode(DistributionFunction.SYNCHROTRON_MODE_NEGLECT)
    ds.eqsys.f_hot.setAdvectionInterpolationMethod(DistributionFunction.AD_INTERP_UPWIND)

    # Set solver type
    ds.solver.setType(Solver.LINEAR_IMPLICIT) # semi-implicit time stepping
    ds.solver.preconditioner.setEnabled(False)

## helper function(s) for plotting DREAM output data

def plotRunawayRate(do, ax=None, label=None, normalize=False, plotTime=False):
    """
    Plot runaway rate vs. time to check convergence.

    DREAM.DREAMOutput do :      DREAM settings object.
    matplotlib.axes.Axes ax :   Axes object used for plotting.
    str label :                 Legend label.
    bool normalize :            Normalize such that runawayRate=1 at time=minorRadius=0.
    bool plotTime :             x=time if True, otherwise x=minorRadius.
    """
    if ax is None:
        ax = plt.axes()

    try:
        data = do.other.fluid.runawayRate.data
    except AttributeError as err:
        raise Exception(f'Output file {fp} does not include .') from err

    if normalize:
        print(data[0,0], data[0])
        data /= data[0,0]

    if plotTime: # runawayRate vs. time
        time = do.other.fluid.runawayRate.time
        runawayRate = data[:,0]
        ax.semilogy(time, runawayRate, label=label)

    else: # runawayRate vs. minorRadius
        minorRadius = do.grid.r
        runawayRate = data[0,:]
        ax.plot(minorRadius, runawayRate, label=label)

    return ax



## If script is run, create default DREAM settings as demo

if __name__ == '__main__':

    # show more information
    if len(sys.argv) == 1:
        verbose = False
    elif sys.argv[1] == '-v':
        verbose = True

    # basic DREAM settings setup
    ds = DREAMSettings()
    configureGrids(ds, verbose=verbose)
    configureEquations(ds, verbose=verbose)
    ds.other.include('fluid/runawayRate')

    # Save settings
    ds.output.setTiming(stdout=True, file=True)
    ds.output.setFilename('outputs/demo_output.h5')
    ds.save('dream_settings/demo_dream_settings.h5')
