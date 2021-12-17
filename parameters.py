"""
Collection of constant parameters used throughout in this project.
"""
import numpy as np
import sys

# make sure path to DREAM exists
DREAM_PATH = '/home/peterhalldestam/DREAM/py'  # /path/to/DREAM/py
try:
    sys.path.append(DREAM_PATH)
    import DREAM
except ModuleNotFoundError as err:
    raise Exception(f'DREAM_PATH={DREAM_PATH} does not exist!') from err

# default parameters
ELECTRON_DENSITY = 5e19 # [m^-3]
ELECTRIC_FIELD = 1.0   # [V/m]
TEMPERATURE = 300   # [eV]

m_e = 510999           # Electron mass [eV/c^2]
MU_0 = 4e-7 * np.pi    # Permeability of free space

PLASMA_CURRENT = 200e3  # Reference plasma current which generates poloidal field

MAJOR_RADIUS = 6.8e-1   # [m]
MINOR_RADIUS = 2.2e-1   # [m]
WALL_RADIUS = 1.2 * MINOR_RADIUS

MAGNETIC_FIELD = 5e0  # on-axis magnetic field strength

# Grid parameter maxima
MAX_MOMENTUM        = 1e2                # max momentum in units of m_e*c, appropiately ~1e2 for avalanche simulations
MAX_PITCH_STEP      = 1e-2               # max pitch step
MAX_TIME            = 2.5e-1             # simulation time in seconds
MAX_SHAFRANOV_SHIFT = 0.1 * MINOR_RADIUS # max Shafranov shift
MAX_TRIANGULARITY   = 0.2                # max triangularity
MAX_ELONGATION      = 1.5                # max elongation


# Grid parameters resolution
N_MOMENTUM        = 150 # no. momentum grid points
N_PITCH           = 50   # no. pitch grid points
N_TIME            = 20 # no. time steps
N_RADIUS          = 20   # no. radial grid points
N_POLODIAL_FLUX   = 20  # no. poloidal flux grid points
N_SHAFRANOV_SHIFT = 20  # no. Shafranov shift grid point
N_TRIANGULARITY   = 20  # no. triangularity grid points
N_ELONGATION      = 20  # no. elongation grid points

# Avalanche parameters including definition of biuniform grid
P_TH            = np.sqrt(2 * TEMPERATURE / m_e)         # thermal momentum of the electrons in units of m_e*c
P_CUT_AVALANCHE = 0.01                                   # minimum momentum to which the Avalanche source term is applied in units of m_e*c
PSEP            = float(7 * P_TH)                        # max momentum of the lower grid in units of m_e*c
N_PSEP          = int(N_MOMENTUM + PSEP - MAX_MOMENTUM)  # no. grid points in the lower grid

# check output parameters
TOL_ELECTRON_DENSITY_RATIO	= 0.01	# tolerance of the ration n_re/n_cold
TOL_RUNAWAY_RATE_CONVERGENCE	= 0.1	# tolerance for the relative convergence of runawayRate
LIM_RUNAWAY_RATE_CONVERGENCE	= 0.8	# percentual limit from which the convergence will be tested
