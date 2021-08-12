"""
Created by Peter Halldestam 12/8/21.

Script used for setting up a linearly implicit solver in DREAM, which solves a
system of equations describing the evolution of a tokamak plasma during a
disruption (url: ft.nephy.chalmers.se/dream).

In terminal run:
    $ python3 settings.py [-g GEOMETRY] [-E E_FIELD] [-T TEMPERATURE] [-p PLOT]

Optional arguments:
    -g int GEOMETRY       Radial grid geometry (cylindrical = 0, toroidal = 1).
    -E float E_FIELD      Electric field strength [V/m].
    -T float TEMPERATURE  Plasma temperature [eV].
    -p bool PLOT          Plot geometry.

To then use the python API, simply run:
    $ /path/to/DREAM/build/iface/dreami dream_settings.h5
    $ /path/to/DREAM/py/cli/cli.py output.h5
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

sys.path.append('../../../../DREAM/py')  # /path/to/DREAM/py
from DREAM.DREAMSettings import DREAMSettings
from DREAM.DREAMSettings import DREAMSettings
import DREAM.Settings.Equations.IonSpecies as Ions
import DREAM.Settings.Equations.RunawayElectrons as Runaways
import DREAM.Settings.Equations.DistributionFunction as DistFunc
import DREAM.Settings.Solver as Solver

# geometry types
CYLINDRICAL_GEOMETRY = 0
TOROIDAL_GEOMETRY = 1

# default parameters
ELECTRIC_FIELD_STRENGTH = 6.0   # [V/m]
TEMPERATURE = 100   # [eV]

# command line parser setup
parser = argparse.ArgumentParser()
parser.add_argument('-geom', type=int, default=CYLINDRICAL_GEOMETRY,
                    help='Radial grid geometry (cylindrical = 0, toroidal = 1).')
parser.add_argument('-efs', type=float, default=ELECTRIC_FIELD_STRENGTH,
                    help='Electric field strength [V/m].')
parser.add_argument('-temp', type=float, default=TEMPERATURE,
                    help='Plasma temperature [eV].')
parser.add_argument('-plot', type=bool, default=False, help='Plot geometry.')
args = parser.parse_args()

# physical parameters
electron_density = 5e19    # Electron density (m^-3)
electric_field_strength = args.efs
temperature = args.temp
geometry = args.geom

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
kappa = np.linspace(0, 0.5, rkappa.size)     # Elongation

# Toroidal field function
GOverR0 = B0       # = R*Bphi/R0

# Poloidal flux
mu0 = 4e-7 * np.pi       # Permeability of free space
IpRef = 200e3            # Reference plasma current which generates poloidal field
psi = -mu0 * IpRef * (1-(rpsi/a)**2) * a


## configure simulation settings ===============================================

ds = DREAMSettings()

# Set up radial grid
if geometry == CYLINDRICAL_GEOMETRY:
    print('setting up a cylindrical geometry')
    ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0)

elif geometry == TOROIDAL_GEOMETRY:
    print('setting up a toroidal geometry (ITER tokamak)')
    ds.radialgrid.setShaping(psi=psi, rpsi=rpsi, GOverR0=GOverR0,
                             kappa=kappa, rkappa=rkappa,
                             Delta=Delta, rDelta=rDelta,
                             delta=delta, rdelta=rdelta)

    # adjust xi-grid
    ds.hottailgrid.setTrappedPassingBoundaryLayerGrid(dxiMax=1e-2)

else:
    help_message = parser._option_string_actions['-geometry'].help
    raise ValueError(f"Illegal -geometry argument!\n\n\t help: {help_message}")

ds.radialgrid.setB0(B0)
ds.radialgrid.setWallRadius(a*1.2)
ds.radialgrid.setMajorRadius(R0)
ds.radialgrid.setMinorRadius(a)
ds.radialgrid.setNr(Nr)

if args.plot:
    ds.radialgrid.visualize_analytic(nr=10, ntheta=100)

# Set E_field
ds.eqsys.E_field.setPrescribedData(electric_field_strength)

# Set temperature
ds.eqsys.T_cold.setPrescribedData(temperature)

# Set ions
ds.eqsys.n_i.addIon(name='D', Z=1, iontype=Ions.IONS_PRESCRIBED_FULLY_IONIZED, n=electron_density)

# Disable avalanche generation
ds.eqsys.n_re.setAvalanche(avalanche=Runaways.AVALANCHE_MODE_NEGLECT)

# Hot-tail grid settings
ds.hottailgrid.setNxi(Nxi)
ds.hottailgrid.setNp(Np)
ds.hottailgrid.setPmax(pMax)

# Set initial hot electron Maxwellian
ds.eqsys.f_hot.setInitialProfiles(n0=electron_density, T0=temperature)

# Set boundary condition type at pMax
ds.eqsys.f_hot.setBoundaryCondition(DistFunc.BC_F_0) # F=0 outside the boundary
ds.eqsys.f_hot.setSynchrotronMode(DistFunc.SYNCHROTRON_MODE_NEGLECT)
ds.eqsys.f_hot.setAdvectionInterpolationMethod(DistFunc.AD_INTERP_UPWIND)

# Disable runaway grid
ds.runawaygrid.setEnabled(False)

# Set solver type
ds.solver.setType(Solver.LINEAR_IMPLICIT) # semi-implicit time stepping
ds.solver.preconditioner.setEnabled(False)

# include otherquantities to save to output
ds.other.include('fluid/runawayRate')

# Set time stepper
ds.timestep.setTmax(tMax)
ds.timestep.setNt(Nt)

# Save settings
ds.output.setTiming(stdout=True, file=True)
ds.output.setFilename('output.h5')
ds.save('dream_settings.h5')
