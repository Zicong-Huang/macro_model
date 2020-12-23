# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 19:15:22 2020

@author: jacob
"""

import matplotlib.pyplot as plt
import numpy as np

#
# AR(1), flip of coin
T = 100
rho = 0.95
x = np.zeros(T)
coin = np.array([1, -1])
for i in range(0, T-1):
    x[i+1] = rho*x[i] + np.random.choice(coin)

fig1,ax = plt.subplots(dpi = 300)
ax.plot(x)
ax.set_xlabel('time')
ax.set_ylabel('x(t)')
ax.set_title('AR(1) simulation of a flip of coin')

#
# two more series
y = np.zeros(T)
z = np.zeros(T)
for i in range(0, T-1):
    y[i+1] = rho*y[i] + np.random.choice(coin)
    z[i+1] = rho*z[i] + np.random.choice(coin)

fig2,ax = plt.subplots(dpi = 300)
ax.plot(x)
ax.plot(y)
ax.plot(z)
ax.set_xlabel('time')
ax.set_ylabel('three series')
ax.set_title('AR(1) simulation of flips of coin')