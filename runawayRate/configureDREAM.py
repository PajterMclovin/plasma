#!/usr/bin/python3
"""
Created by Peter Halldestam 19/8/21,
modified by Hannes Bergström 26/8/21,
modified by Peter Halldestam 4/9/21,
modified by Hannes Bergström 8/9/21.
modified by Hannes Bergström 25/11/21.
"""
import sys, os
import numpy as np
import matplotlib.pyplot as plt

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import (quite a few...)
sys.path.append(os.path.join(dir, '..'))
import parameters as p

# Settings object imports
sys.path.append(p.DREAM_PATH)
from DREAM.DREAMSettings import DREAMSettings
from DREAM.Settings.Equations.IonSpecies import IONS_PRESCRIBED_FULLY_IONIZED
from DREAM.Settings.Equations.DistributionFunction import BC_F_0
from DREAM.Settings.Equations.DistributionFunction import SYNCHROTRON_MODE_NEGLECT
from DREAM.Settings.Equations.DistributionFunction import AD_INTERP_UPWIND, AD_INTERP_TCDF, AD_INTERP_JACOBIAN_UPWIND
from DREAM.Settings.Solver import LINEAR_IMPLICIT, NONLINEAR, LINEAR_SOLVER_MKL
from DREAM.Settings.Equations.RunawayElectrons import DREICER_RATE_NEURAL_NETWORK
# Geometries
CYLINDRICAL = 1
TOROIDAL = 2
#NUMERICAL = 3

# Avalanche runaway settings
AVALANCHE_NEGLECT   = 1
AVALANCHE_FLUID     = 2
AVALANCHE_KINETIC   = 4
AVALANCHE_TRAPPING_NEGLECT = 1
AVALANCHE_TRAPPING_INCLUDE = 2

class ConfigureDREAM:

    def __init__(self, output='output.h5', save='settings.h5', **kwargs):
        """
        Initializes an object for dealing with the configuration of a single
        DREAMSettings object. See DREAM/py/DREAM/DREAMSettings.py

        OPTIONAL KEYWORD ARGUMENTS:
            str output :                Name of DREAM output object save file.
            str save :                  Name of DREAM settings object save file.
            bool verbose :              Show information.
            DREAMSettings ds :          Settings object.
            str include :               Or list of strings, other quantities to include.
            int geometry :              Geometry type.
            float minorRadius :         Prescribed minor radius of the magnetic field.
            float majorRadius :         Prescribed major radius of the magnetic field.
            float wallRadius :          Prescribed wall radius of the device.
            float electricField :       Prescribed electric field strength.
            float temperature :         Prescribed temperature.
            float maxElongation :       Shaping parameter.
            float maxTriangularity :    Shaping parameter.
            float maxShafranovShift :   Shaping parameter.
            tuple ion :                 Name and proton number pair describing the type of ion used in the plasma.
            bool avalanche :            If True, configures avalanche generation and appropriate biuniform grid.

        """
        self.verbose            = kwargs.get('verbose',             False)
        self.ds                 = kwargs.get('ds',                  None)
        self.include            = kwargs.get('include',             None)
        self.geometry           = kwargs.get('geometry',            TOROIDAL)
        self.minorRadius        = kwargs.get('minorRadius',         p.MINOR_RADIUS)
        self.majorRadius        = kwargs.get('majorRadius',         p.MAJOR_RADIUS)
        self.wallRadius         = kwargs.get('wallRadius',          p.WALL_RADIUS)
        self.electricField      = kwargs.get('electricField',       p.ELECTRIC_FIELD)
        self.temperature        = kwargs.get('temperature',         p.TEMPERATURE)
        self.maxElongation      = kwargs.get('maxElongation',       p.MAX_ELONGATION)
        self.maxTriangularity   = kwargs.get('maxTriangularity',    p.MAX_TRIANGULARITY)
        self.maxShafranovShift  = kwargs.get('maxShafranovShift',   p.MAX_SHAFRANOV_SHIFT)
        self.ion                = kwargs.get('ion',                 ('D', 1))
        self.avalanche          = kwargs.get('avalanche',           AVALANCHE_NEGLECT)
        self.avaTrapping        = kwargs.get('avaTrapping',         AVALANCHE_TRAPPING_NEGLECT)

        # Creattope and configure DREAM settings
        if self.ds is None:
            self.ds = DREAMSettings()
            self.configureGrids()
            self.configureEquations()

        # include other quantities
        if self.include is not None:
            if type(self.include) is list:
                for quantity in self.include:
                    self.ds.other.include(quantity)
            else:
                self.ds.other.include(self.include)

        # prepare simulation
        self.ds.output.setTiming(stdout=True, file=True)
        self.ds.output.setFilename(output)
        self.ds.save(save)



    ## helper functions for configuring DREAM settings

    def setToroidal(self):
        """
        Setting up a toroidal geometry.
        """
        if self.verbose:
            print(self.setToroidal.__doc__)

        ds = self.ds

        # set type to 2
        ds.radialgrid.setType(TOROIDAL)

        # Set shaping parameters
        kappa = np.linspace(0, self.maxElongation, p.N_ELONGATION)
        delta = np.linspace(0, self.maxTriangularity, p.N_TRIANGULARITY)
        Delta = np.linspace(0, self.maxShafranovShift, p.N_SHAFRANOV_SHIFT)

        # Set up input radial grids
        rkappa = np.linspace(0, self.minorRadius, p.N_ELONGATION)
        rdelta = np.linspace(0, self.minorRadius, p.N_TRIANGULARITY)
        rDelta = np.linspace(0, self.minorRadius, p.N_SHAFRANOV_SHIFT)

        # Toroidal field function
        GOverR0 = p.MAGNETIC_FIELD     # = R*Bphi/R0

        # Poloidal flux
        rpsi = np.linspace(0, self.minorRadius, p.N_POLODIAL_FLUX)
        psi = -p.MU_0 * p.PLASMA_CURRENT * (1-(rpsi / self.minorRadius)**2) * self.minorRadius

        # set radial grid shape
        ds.radialgrid.setMajorRadius(self.majorRadius)
        ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0,
                                 kappa=kappa, rkappa=rkappa,
                                 Delta=Delta, rDelta=rDelta,
                                 delta=delta, rdelta=rdelta)

        # automatically adjust xi-grid
        ds.hottailgrid.setTrappedPassingBoundaryLayerGrid(dxiMax=p.MAX_PITCH_STEP)


    def configureGrids(self):
        """
        Configuring grids in DREAM settings object.
        """
        if self.verbose:
            print(self.configureGrids.__doc__)

        ds = self.ds

        if self.geometry == CYLINDRICAL:
            if self.verbose:
                print('Setting up a cylindrical geometry.')

            # set type to 1 and on-axis magnetic field strength
            ds.radialgrid.setType(CYLINDRICAL)
            ds.radialgrid.setB0(p.MAGNETIC_FIELD)

        elif self.geometry == TOROIDAL:
            self.setToroidal()
        else:
            raise ValueError("Invalid geometry input!")

        # general radial grid settings
        ds.radialgrid.setWallRadius(self.wallRadius)
        ds.radialgrid.setMinorRadius(self.minorRadius)
        ds.radialgrid.setNr(p.N_RADIUS)

        # hot-tail and runaway grid settings
        if self.avalanche == AVALANCHE_KINETIC:
            ds.hottailgrid.setNxi(p.N_PITCH)
            ds.hottailgrid.setNp(p.N_PSEP)
            ds.hottailgrid.setPmax(p.PSEP)
            ds.runawaygrid.setEnabled(True)
            ds.runawaygrid.setNxi(p.N_PITCH)
            ds.runawaygrid.setNp(p.N_MOMENTUM-p.N_PSEP)
            ds.runawaygrid.setPmax(p.MAX_MOMENTUM)
        else:

#            ds.hottailgrid.setNxi(p.N_PITCH)
#            ds.hottailgrid.setNp(p.N_MOMENTUM)
#            ds.hottailgrid.setPmax(p.MAX_MOMENTUM)


            ds.hottailgrid.setEnabled(False)
            # ds.runawaygrid.setEnabled(True)
            # ds.runawaygrid.setNxi(p.N_PITCH)
            # ds.runawaygrid.setNp(p.N_MOMENTUM)
            # ds.runawaygrid.setPmax(p.MAX_MOMENTUM)
            ds.runawaygrid.setEnabled(False)


        # time grid settings
        ds.timestep.setTmax(p.MAX_TIME)
        ds.timestep.setNt(p.N_TIME)


    def configureEquations(self):
        """
        Configuring equation system in DREAM settings object. This method is
        subject to change if/when further configurations are needed.
        """
        if self.verbose:
            print(self.configureEquations.__doc__)

        ds = self.ds

        ds.eqsys.E_field.setPrescribedData(self.electricField)
        ds.eqsys.T_cold.setPrescribedData(self.temperature)

        # Set initial hot electron Maxwellian
        ds.eqsys.f_hot.setInitialProfiles(n0=p.ELECTRON_DENSITY, T0=self.temperature)

        # Set ions
        ds.eqsys.n_i.addIon(name=self.ion[0], Z=self.ion[1], n=p.ELECTRON_DENSITY/self.ion[1],
                            iontype=IONS_PRESCRIBED_FULLY_IONIZED)

        ds.eqsys.n_re.setDreicer(DREICER_RATE_NEURAL_NETWORK)

        # Configure avalanche generation
        if self.avalanche == AVALANCHE_KINETIC:
            pCut = p.P_CUT_AVALANCHE
            ds.solver.setType(NONLINEAR)
            ds.solver.setLinearSolver(LINEAR_SOLVER_MKL)
            ds.eqsys.f_re.setAdvectionInterpolationMethod(ad_int=AD_INTERP_TCDF, ad_jac=AD_INTERP_JACOBIAN_UPWIND)
        else:
            pCut = 0
            ds.solver.setType(LINEAR_IMPLICIT)

        # ds.eqsys.n_re.setAvalanche(avalanche=self.avalanche, pCutAvalanche=pCut)
        ds.eqsys.n_re.setAvalanche(avalanche=self.avalanche, pCutAvalanche=pCut, avaTrapping=self.avaTrapping)


        # Set boundary condition type at pMax
        ds.eqsys.f_hot.setBoundaryCondition(BC_F_0) # F=0 outside the boundary
        ds.eqsys.f_hot.setSynchrotronMode(SYNCHROTRON_MODE_NEGLECT)
        ds.eqsys.f_hot.setAdvectionInterpolationMethod(ad_int=AD_INTERP_UPWIND)
        # ds.eqsys.f_hot.setAdvectionInterpolationMethod(ad_int=AD_INTERP_TCDF, ad_jac=AD_INTERP_JACOBIAN_UPWIND)

        # Set solver type
        ds.solver.preconditioner.setEnabled(False)




if __name__ == '__main__':

    ConfigureDREAM(include='fluid/runawayRate', verbose=(len(sys.argv)==2))
