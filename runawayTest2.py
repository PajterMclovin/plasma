#!/usr/bin/env python3
'''
Created by Peter Halldestam 24/1/22

2nd version

Effect of toroidicity, reproduction of fig. 6 in paper:
(E Nilsson et al 2015 Plasma Phys. Control. Fusion 57 095006)

'''


import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy import constants

sys.path.append('/home/pethalld/DREAM/py') # Modify this path as needed on your system
from DREAM import DREAMSettings, runiface
import DREAM.Settings.RadialGrid as RadialGrid
import DREAM.Settings.Equations.IonSpecies as Ions
import DREAM.Settings.Solver as Solver
import DREAM.Settings.Equations.RunawayElectrons as Runaways
import DREAM.Settings.Equations.DistributionFunction as DistFunc
import DREAM.Settings.Equations.HotElectronDistribution as FHot

import DREAM.Settings.CollisionHandler as Collisions

from DREAM.Formulas.PlasmaParameters import getEc

HOTTAIL = False

# plasma parameters
n = 2e19    # Electron density (m^-3)
T = 5e2     # Temperature (eV)
E = 40 * getEc(T, n)       # Electric field strength (V/m)

# Grid parameters
pMax = 1    # maximum momentum in units of m_e*c
Np   = 60  # number of momentum grid points
Nxi  = 30   # number of pitch grid points
nr   = 10    # number of radial grid points
tMax = 7e-1 # simulation time in seconds
Nt   = 10   # number of time steps

# Tokamak Parameters
a = 1#2.2e-1         # minor radius [m]
b = a * 1.2    # wall radius [m]
R0 = a/.9 #6.8e-1        # major radius [m]
B0 = 5e0        # on-axis magnetic field [T]

IpRef = 200e3

def generate(majorRadius):
    ds = DREAMSettings()

    # constant plasma parameters
    ds.eqsys.E_field.setPrescribedData(E)
    ds.eqsys.T_cold.setPrescribedData(T)
    ds.eqsys.n_i.addIon(name='D', Z=1, n=n, iontype=Ions.IONS_PRESCRIBED_FULLY_IONIZED)

    ds.eqsys.n_re.setAvalanche(Runaways.AVALANCHE_MODE_NEGLECT)


    if HOTTAIL:
        # Hot-tail grid settings
        ds.hottailgrid.setNxi(Nxi)
        ds.hottailgrid.setNp(Np)
        ds.hottailgrid.setPmax(pMax)

        # Set initial hot electron Maxwellian
        ds.eqsys.f_hot.setInitialProfiles(n0=n, T0=T)

        # Set boundary condition type at pMax
        ds.eqsys.f_hot.setBoundaryCondition(FHot.BC_F_0) # F=0 outside the boundary

        ds.eqsys.f_hot.setParticleSource(FHot.PARTICLE_SOURCE_EXPLICIT)

        # automatically adjust xi-grid
        ds.hottailgrid.setTrappedPassingBoundaryLayerGrid(dxiMax=1e-2)
        # ds.eqsys.f_hot.setBoundaryCondition(DistFunc.BC_F_0) # F=0 outside the boundary
        # ds.eqsys.f_hot.setSynchrotronMode(DistFunc.SYNCHROTRON_MODE_NEGLECT)
        # ds.eqsys.f_hot.setAdvectionInterpolationMethod(ad_int=DistFunc.AD_INTERP_TCDF, ad_jac=DistFunc.AD_INTERP_JACOBIAN_UPWIND)
        #
        # # Set solver type
        # ds.solver.setType(Solver.NONLINEAR) # semi-implicit time stepping
        # ds.solver.preconditioner.setEnabled(False)

    else:
        # use neural network, no kinetic grid?
        ds.hottailgrid.setEnabled(False)
        ds.eqsys.n_re.setDreicer(Runaways.DREICER_RATE_NEURAL_NETWORK)
    ds.solver.setType(Solver.LINEAR_IMPLICIT)

    ds.runawaygrid.setEnabled(False)

    if np.isinf(majorRadius):
        ds.radialgrid.setType(RadialGrid.TYPE_CYLINDRICAL)
        ds.radialgrid.setB0(B0)

    else:
        # radial grid, circular plasma
        ds.radialgrid.setType(RadialGrid.TYPE_ANALYTIC_TOROIDAL)


        # Poloidal flux
        mu0 = constants.mu_0
        rref = np.linspace(0, a, 20)
        psiref = -mu0 * IpRef * (1-(rref / a)**2) * a

        # set radial grid shape
        ds.radialgrid.setShaping(psi=psiref, rpsi=rref, GOverR0=B0)

    ds.radialgrid.setNr(nr)
    ds.radialgrid.setMinorRadius(a)
    ds.radialgrid.setWallRadius(b)
    ds.radialgrid.setMajorRadius(majorRadius)

    ds.other.include('fluid')

    ds.timestep.setTmax(tMax)
    ds.timestep.setNt(Nt)
    return ds

# ## cylindrical limit, epsilon = 0
# dsCyl = generate(np.inf)
# do = runiface(dsCyl, 'output_cyl.h5', quiet=False)
# gamma0 = do.other.fluid.runawayRate.data[-1,:].mean()
# print(gamma0)

## toroidal, epsilon > 0
dsTor = generate(R0)
do = runiface(dsTor, 'output_tor.h5', quiet=False)

do.other.fluid.runawayRate.plot(t=-1)
plt.show()
