#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('/home/pethalld/DREAM/py') # Modify this path as needed on your system
from DREAM import DREAMSettings, runiface
import DREAM.Settings.RadialGrid as RadialGrid
import DREAM.Settings.Equations.IonSpecies as Ions
import DREAM.Settings.Solver as Solver
import DREAM.Settings.Equations.RunawayElectrons as Runaways

# radial grid resolution
nr = 100

# plasma parameters
T_profile = 1e2 * np.ones(nr)
ne_profile = 5e19 * np.ones(nr)
E_profile = 1.0 * np.ones(nr)

# Tokamak Parameters
a = 2.0         # minor radius [m]
b = a * 1.35    # wall radius [m]
R0 = 100.0        # major radius [m]
B0 = 5.3        # on-axis magnetic field [T]
r = np.linspace(0, a, nr)

Ip = 200e3

### 1. calculate conductivity
ds = DREAMSettings()

# radial grid
ds.radialgrid.setType(RadialGrid.TYPE_ANALYTIC_TOROIDAL)

# Set shaping parameters
kappa = np.linspace(1, 1, nr)
delta = np.linspace(0, .2, nr)*0
Delta = np.linspace(0, .1 * a, nr)*0

# Set up input radial grids
rkappa = np.linspace(0, a, nr)
rdelta = np.linspace(0, a, nr)
rDelta = np.linspace(0, a, nr)

# Toroidal field function
GOverR0 = B0

# Poloidal flux
rpsi = np.linspace(0, a, nr)
psi = -4e-7 * np.pi * Ip * (1-(rpsi / a)**2) * a

# set radial grid shape
ds.radialgrid.setMajorRadius(R0)
ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0,
                         kappa=kappa, rkappa=rkappa,
                         Delta=Delta, rDelta=rDelta,
                         delta=delta, rdelta=rdelta)

ds.radialgrid.setNr(nr)
ds.radialgrid.setMinorRadius(a)
ds.radialgrid.setWallRadius(b)

ds.radialgrid.visualize()

# no kinetic grids
ds.hottailgrid.setEnabled(False)
ds.runawaygrid.setEnabled(False)

# constant plasma parameters
ds.eqsys.E_field.setPrescribedData(E_profile, radius=r)
ds.eqsys.T_cold.setPrescribedData(T_profile, radius=r)
ds.eqsys.n_i.addIon(name='D', Z=1, n=ne_profile, r=r, iontype=Ions.IONS_PRESCRIBED_FULLY_IONIZED)

# solver
ds.solver.setLinearSolver(Solver.LINEAR_SOLVER_LU)
ds.solver.setType(Solver.NONLINEAR)

# set runaway generation models
ds.eqsys.n_re.setAvalanche(Runaways.AVALANCHE_MODE_FLUID)
ds.eqsys.n_re.setDreicer(Runaways.DREICER_RATE_NEURAL_NETWORK)

###
ds.timestep.setTmax(2e-2)
ds.timestep.setNt(10)

ds.other.include('fluid')

# Calculate conductivity
do = runiface(ds, 'output.h5', quiet=False)

gammaDreicer = do.other.fluid.gammaDreicer.data[-1,:]
runawayRate = do.other.fluid.runawayRate.data[-1,:]
GammaAva = (runawayRate - gammaDreicer) / do.eqsys.n_re[-1,:]
plt.plot(do.other.fluid.GammaAva.data[-1,:])
plt.show()
