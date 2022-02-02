#!/usr/bin/python3
"""
Created by Peter Halldestam 24/1/22.

Plot of eq. 3 in project report.
"""
import sys, os
import numpy as np
import matplotlib.pyplot as plt

dir = os.path.dirname(os.path.realpath(__file__))

# Parameters import (quite a few...)
sys.path.append(os.path.join(dir, '../..'))
import parameters as p


def trapped(eps):
    a = p.MINOR_RADIUS
    R0 = p.MAJOR_RADIUS
    dMax = 0#p.MAX_TRIANGULARITY
    DMax = 0#p.MAX_SHAFRANOV_SHIFT
    print(a, R0, dMax, DMax)
    return eps*(1-np.sin(dMax*eps*R0/a))/(1+eps*(1+DMax/a))

def nilssonFit(eps):
    return 1-1.2*np.sqrt(2*eps/(1+eps))

eps = np.linspace(0, 1)
plt.plot(eps, np.sqrt(1-trapped(eps)), '-')
plt.plot(eps, nilssonFit(eps), '.-')
plt.show()
