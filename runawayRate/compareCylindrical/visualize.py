#!/bin/python3 -i

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append('../../../../DREAM/py')  # /path/to/DREAM/py

from DREAM import *
from DREAM.DREAMOutput import DREAMOutput


do = None
if len(sys.argv) == 1:
    do = DREAMOutput('output.h5')
elif len(sys.argv) == 2:
    do = DREAMOutput(sys.argv[1])
else:
    print('ERROR: Invalid command line arguments. Expected at most one argument.')
    sys.exit(1)


# do.eqsys.E_field.plotRadialProfile(t=0)
time = do.other.fluid.runawayRate.time
radius = do.other.fluid.runawayRate.radius
runawayRates = do.other.fluid.runawayRate.data



for fp in os.listdir('./outputs/'):
    if fp.endswith(".h5"):
        print(fp)
        continue
    else:
        continue
