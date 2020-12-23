# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 11:40:53 2020

@author: Zicong Huang
"""

import numpy as np
import matplotlib.pyplot as plt

# set initial inputs
K0 = 1    # initial capital stock
Y0 = 1.1     # initial TFP
N0 = 1      # initial population

# set model parameters
alpha = 0.33        # capital income share of output
delta = 0.10        # depreciation rate
s = 0.20            # saving rate
n = 0.01            # population growth rate
T = 25              # periods simulated
start_year = 2000

# initial value of output
A0 = Y0/((K0**alpha)*(N0**(1-alpha)))

# initialize time series
K_N = np.zeros(T)
N = np.zeros(T)
K_N[0] = K0/N0
N[0] = N0
A = np.zeros(T)
A[0] = A0

# simulate the model
for t in range(0, T-1):
    N[t+1] = (1 + n) * N[t]
    K_N[t+1] = ((1-delta)/(1+n)) * K_N[t] + (s/(1+n)) * A0 * K_N[t]

for t in range(1, T):
    A[t] = A0 * (K_N[t] ** (1-alpha))

# compute
Y_N = A * (K_N ** alpha)
K = K_N * N
wages = (1-alpha) * A * (K ** (alpha)) * (N ** (-alpha))
rental_rate = alpha * A * (K ** (alpha-1)) * (N ** (1-alpha))


# plots
year = np.arange(start_year, start_year + T)

fig0, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K_N)
ax.set_ylabel(r'$k_t$', rotation=0)
ax.set_xlabel(r'$t$')
ax.set_title('AK model: capital-to-labor ratio')

fig1, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y_N)
ax.set_ylabel(r'$y_t$', rotation=0)
ax.set_xlabel(r'$t$')
ax.set_title('AK model: output per labor')

fig2, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, A)
ax.set_ylabel(r'$A$', rotation=0)
ax.set_xlabel(r'$t$')
ax.set_title('AK model: TFP')

fig3, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, np.log(K_N))
ax.set_ylabel(r'$ln(k)$', rotation=0)
ax.set_xlabel(r'$t$')
ax.set_title('AK model: log capital-to-labor ratio')

fig4, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, wages, label = 'wages')
ax.plot(year, rental_rate, label = 'rental rates')
ax.set_ylabel('real value')
ax.set_xlabel(r'$t$')
ax.set_title('AK model: wages')
ax.legend()