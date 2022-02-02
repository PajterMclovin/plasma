import numpy as np
import matplotlib.pyplot as plt

from scipy.special import erf

def erfDer(x):
    ''' Derivative of the error function '''
    return 2 * np.exp(-x**2) / np.sqrt(np.pi)

def chskr(x):
    ''' Chandrasekhar function '''
    return (erf(x) - x * erfDer(x)) / (2 * x**2)


# set font sizes
SMALL_SIZE = 14
MEDIUM_SIZE = 16
# BIGGER_SIZE = 18
plt.rc('font', size=SMALL_SIZE)          # default
plt.rc('axes', titlesize=SMALL_SIZE)     # axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # x tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # y tick labels

# figure size (import this)
FIGSIZE = (6, 5)
fig = plt.figure(figsize=FIGSIZE)

x0, x1 = .01, 5
x = np.linspace(x0, x1, 1000)
plt.plot(x, chskr(x), 'k')
plt.plot([0, x0], [0, chskr(x0)], 'k')

xc = 3
plt.plot([0, xc], [chskr(xc), chskr(xc)], '--', c='grey')
plt.plot([xc, xc], [0, chskr(xc)], '--', c='grey')

plt.plot(x, (1/x**2) * chskr(x1) * x1**2, 'k--')

x = np.linspace(0, x1)
plt.plot(x, x * chskr(x0) / x0, 'k--')


plt.xlim(0, x1)
plt.ylim(0, .25)

plt.xticks([1, xc], labels=[r'$v_{th}$', r'$v_c$'])
plt.yticks([chskr(xc)], labels=[r'$eE_\parallel$'])

# plt.xlabel(r'$v$')
# plt.ylabel(r'$F_{drag}$')
plt.xlabel('velocity')
plt.ylabel('drag force')

plt.text(.05, .2, r'$\sim v$', fontsize=SMALL_SIZE)
plt.text(1.9, .15, r'$\sim\frac{1}{v^2}$', fontsize=SMALL_SIZE)

plt.show()
