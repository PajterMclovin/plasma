#!/usr/bin/env python3
"""
Created by Peter Halldestam 20/1/22.

Effect of toroidicity, reproduction of fig. 6 in paper:
(E Nilsson et al 2015 Plasma Phys. Control. Fusion 57 095006)

"""


import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('/home/pethalld/DREAM/py') # Modify this path as needed on your system
from DREAM import DREAMOutput


try:
    doCyl = DREAMOutput('output_cyl.h5')
    doTor = DREAMOutput('output_tor.h5')
except FileNotFoundError :
    print('Output files from inputDreicer.py required. Run this script first!')
    exit(1)


gammaCyl = doCyl.other.fluid.runawayRate.data[-1,:].mean()
# print(gammaCyl.std(), gammaCyl.max()-gammaCyl.min())
gammaTor = doTor.other.fluid.runawayRate.data[-1,:]

plt.plot(gammaTor/gammaCyl)

eps = np.linspace(0, 1)
plt.plot(eps, 1-1.2*np.sqrt((2*eps)/(1+eps)))

plt.show()
