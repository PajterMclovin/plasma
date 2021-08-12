#!/usr/bin/env python3
#
# This example shows how to set up a simple CODE-like runaway
# scenario in DREAM. The simulation uses a constant temperature,
# density and electric field, and generates a runaway current
# through the electric field acceleration, demonstrating Dreicer generation.
#
# Run as
#
#   $ ./intro.py
#   $ ~/DREAM/build/iface/dreami dream_settings.h5
#   $ ~/DREAM/py/cli/cli.py output.h5
#
# ###################################################################

import numpy as np
import sys

sys.path.append('../../../DREAM/py/')

from DREAM.DREAMSettings import DREAMSettings
import DREAM.Settings.Equations.DistributionFunction as DistFunc
import DREAM.Settings.Equations.IonSpecies as Ions
import DREAM.Settings.Equations.RunawayElectrons as Runaways
import DREAM.Settings.Solver as Solver
import DREAM.Settings.CollisionHandler as Collisions
import DREAM.Settings.RadialGrid as RGrid   ## !!

ds = DREAMSettings()
#ds.collisions.collfreq_type = Collisions.COLLFREQ_TYPE_COMPLETELY_SCREENED
ds.collisions.collfreq_type = Collisions.COLLFREQ_TYPE_PARTIALLY_SCREENED

# Physical parameters
E = 6       # Electric field strength (V/m)
n = 5e19    # Electron density (m^-3)
T = 100     # Temperature (eV)

# Grid parameters
pMax = 1    # maximum momentum in units of m_e*c
Np   = 300  # number of momentum grid points
Nxi  = 20   # number of pitch grid points
tMax = 1e-3 # simulation time in seconds
Nt   = 20   # number of time steps
Nr   = 10   # number of radial grid points


# Basic tokamak parameters
a  = 0.22
R0 = 0.68
B0 = 5.0

# Set up input radial grids
rDelta = np.linspace(0, a, 20)
rdelta = np.linspace(0, a, 20)
rkappa = np.linspace(0, a, 20)
rpsi   = np.linspace(0, a, 20)

# Set shaping parameters
Delta = np.linspace(0, 0.1*a, rDelta.size)   # Shafranov shift
delta = np.linspace(0, 0.2, rdelta.size)     # Triangularity
kappa = np.linspace(0, .5, rkappa.size)     # Elongation

# Toroidal field function
GOverR0 = B0       # = R*Bphi/R0

# Poloidal flux
mu0 = 4e-7 * np.pi       # Permeability of free space
IpRef = 200e3            # Reference plasma current which generates poloidal field
psi = -mu0 * IpRef * (1-(rpsi/a)**2) * a

##

# Set E_field
ds.eqsys.E_field.setPrescribedData(E)

# Set temperature
ds.eqsys.T_cold.setPrescribedData(T)

# Set ions
ds.eqsys.n_i.addIon(name='D', Z=1, iontype=Ions.IONS_PRESCRIBED_FULLY_IONIZED, n=n)

# Disable avalanche generation
ds.eqsys.n_re.setAvalanche(avalanche=Runaways.AVALANCHE_MODE_NEGLECT)

# Hot-tail grid settings
ds.hottailgrid.setNxi(Nxi)
ds.hottailgrid.setNp(Np)
ds.hottailgrid.setPmax(pMax)
ds.hottailgrid.setTrappedPassingBoundaryLayerGrid(dxiMax=1e-2)

# Set initial hot electron Maxwellian
ds.eqsys.f_hot.setInitialProfiles(n0=n, T0=T)

# Set boundary condition type at pMax
#ds.eqsys.f_hot.setBoundaryCondition(DistFunc.BC_PHI_CONST) # extrapolate flux to boundary
ds.eqsys.f_hot.setBoundaryCondition(DistFunc.BC_F_0) # F=0 outside the boundary
ds.eqsys.f_hot.setSynchrotronMode(DistFunc.SYNCHROTRON_MODE_NEGLECT)
ds.eqsys.f_hot.setAdvectionInterpolationMethod(DistFunc.AD_INTERP_UPWIND)

# Disable runaway grid
ds.runawaygrid.setEnabled(False)

# Set up radial grid
ds.radialgrid.setB0(B0)
ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0, kappa=kappa,
    rkappa=rkappa, Delta=Delta, rDelta=rDelta, delta=delta, rdelta=rdelta)
ds.radialgrid.setWallRadius(a*1.1)
ds.radialgrid.setMajorRadius(R0)
ds.radialgrid.setMinorRadius(a)
ds.radialgrid.setNr(Nr)

ds.radialgrid.visualize_analytic()  # titta på magnetfältet!

# Set solver type
ds.solver.setType(Solver.LINEAR_IMPLICIT) # semi-implicit time stepping
ds.solver.preconditioner.setEnabled(False)

# include otherquantities to save to output
ds.other.include('fluid/runawayRate')

# Set time stepper
ds.timestep.setTmax(tMax)
ds.timestep.setNt(Nt)

ds.output.setTiming(stdout=True, file=True)
ds.output.setFilename('output.h5')

Save settings to HDF5 file
ds.save('dream_settings.h5')
