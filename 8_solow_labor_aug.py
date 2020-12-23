# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 14:32:22 2020

@author: zicong huang

This program simulate the solow model with labor-augmenting technology
"""

import numpy as np
import matplotlib.pyplot as plt

#
# set initial inputs
K0 = 10          # initial capital stock
A0 = 4         # initial output
N0 = 1          # initial population
E0 = 1          # initial labor-effectiveness

#
# set model parameter
alpha = 0.36        # capital income share of output
delta = 0.08        # depreciation rate
s = 0.30            # saving rates
n = 0.0015           # popuplation growth
g = 0.01               # technology growth (g=0 for baseline solow)
T = 100             # periods simulated
start_year = 2000   # simulation start year

#
# back out value of A
Y0 = A0 * (K0**(alpha)) * ((E0*N0)**(1-alpha))

#
# initialize time series
K_EN = np.zeros(T)          # capital per effective labor
N = np.zeros(T)
E = np.zeros(T)
K_EN[0] = K0 / (E0 * N0)
N[0] = N0
E[0] = E0
EN = E * N                 # effective labor 

#
# simulate the model
for t in range(0,T-1):
    K_EN[t+1] = ((1-delta)/((1+g)*(1+n)))*K_EN[t] + (s/((1+g)*(1+n)))*A0*(K_EN[t]**alpha)
    N[t+1] = (1+n) * N[t]
    E[t+1] = (1+g) * E[t]

EN = E*N

#
# compute a bunch of values
Y_EN = A0 * (K_EN ** alpha)
Y_N = Y_EN * E
Y = Y_N * N

K_N = K_EN * E
K = K_N * N

wage = alpha * A0 * (K**(1-alpha)) * (N**(alpha-1)) * (E ** alpha)
rent = (1-alpha) * A0 * (K**(-alpha)) * ((E * N) **alpha)

#
# steady state
K_EN_ss = ((s*A0)/((1+g)*(1+n)-(1-delta))) ** (1/(1-alpha))
Y_EN_ss = A0 * (K_EN_ss ** alpha)

K_N_ss = K_EN_ss * E
Y_N_ss = Y_EN_ss * E

K_ss = K_N_ss * N
Y_ss = Y_N_ss * N

wage_ss = alpha * A0 * (K_ss**(1-alpha)) * (N**(alpha-1)) * (E ** alpha)
rent_ss = (1-alpha) * A0 * (K_ss**(-alpha)) * ((E * N) **alpha)

#
# solow diagram 1
TT = 100
kk = np.arange(0, TT)
outflow = kk * (g + n + delta)
inflow = s * A0 * (kk ** alpha)
output_pel = A0 * (kk ** alpha)     # output per effective labor
kk_ss = np.argwhere(np.diff(np.sign(inflow - outflow))).flatten() # find intersection: steady state

#
# solow diagram 2
kk_t1 = np.arange(0, TT)
kk_t2 = np.zeros(TT)
for t in range(0,TT):
    kk_t2[t] = ((1-delta)*kk_t1[t])/((1+g)*(1+n)) + (s*A0*(kk_t1[t] ** alpha))/((1+g)*(1+n))

kk_ss2 = np.argwhere(np.diff(np.sign(kk_t2 - kk_t1))).flatten() # find intersection: steady state

#
# plots
year = np.arange(start_year, start_year+T)

fig0, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(kk, inflow, label = r'$sf(\tilde{k})$')
ax.plot(kk, output_pel, label = r'$f(\tilde{k})$')
ax.plot(kk, outflow, label = r'($n+g+\delta)\tilde{k}$')
if len(kk_ss) == 2:
    kk_ss = kk_ss[1]
    inflow_ss = inflow[kk_ss]
    output_pel_ss = output_pel[kk_ss]
    
    ax.vlines(kk_ss, 0, output_pel_ss, linestyles = 'dotted', colors = 'black')
    ax.hlines(inflow_ss, 0, kk_ss, linestyles = 'dotted', colors = 'black')
    ax.hlines(output_pel_ss, 0, kk_ss, linestyles = 'dotted', colors = 'black')
ax.set_xlim(xmin = 0)
ax.set_ylim(ymin = 0)
ax.legend()
ax.set_xlabel(r'$\tilde{k}$')
ax.set_ylabel('values')
ax.set_title('solow diagram 1')


motion = r'$\widetilde{k_{t+1}}=\frac{(1-\delta)}{(1+n) \times (1+g)} \times \widetilde{k_{t}} + \frac{s \times A}{(1+n) \times (1+g)} \times \widetilde{k_{t}}^\alpha $'
fig1, ax = plt.subplots(figsize = (6,6), dpi = 300)
ax.plot(kk_t1,kk_t2, label = motion)
xx = np.linspace(*ax.get_xlim()) # linspace: evenly spaced numbers of a specified intervals
ax.plot(xx, xx, label = r'$45^\circ$') # star expression: pass all items as arguments
plt.axis('scaled')
ax.set_xlim(xmin = 0)
ax.set_ylim(ymin = 0)
if len(kk_ss2) == 2:
    kk_ss2 = kk_ss2[1]
    ax.vlines(kk_ss2, 0, kk_ss2, linestyles = 'dotted', colors = 'black')
    ax.hlines(kk_ss2, 0, kk_ss2, linestyles = 'dotted', colors = 'black')
ax.legend(prop={'size': 12})
ax.set_xlabel(r'$\widetilde{k_{t}}$')
ax.set_ylabel(r'$\widetilde{k_{t+1}}$')
ax.set_title('solow diagram 2')

fig2, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K_EN)
ax.hlines(K_EN_ss, min(year), max(year), linestyles = 'dashed', colors = 'red',
         label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel(r'$\widetilde{k_t}$', rotation=0)
ax.set_title('simulated time path of capital to effective labor')
ax.legend()

fig3, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K_N)
ax.plot(year, K_N_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel(r'$k_t$', rotation=0)
ax.set_title('simulated time path of capital to labor')
ax.legend()

fig4, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K)
ax.plot(year, K_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel(r'$K_t$', rotation=0)
ax.set_title('simulated time path of capital stock')
ax.legend()

fig5, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y_EN)
ax.hlines(Y_EN_ss, min(year), max(year), linestyles = 'dashed', colors = 'red',
         label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel(r'$\widetilde{y_t}$', rotation=0)
ax.set_title('simulated time path of output to effective labor')
ax.legend()

fig6, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y_N)
ax.plot(year, Y_N_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel(r'$y_t$', rotation=0)
ax.set_title('simulated time path of output to labor')
ax.legend()

fig7, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y)
ax.plot(year, Y_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel(r'$Y_t$', rotation=0)
ax.set_title('simulated time path of real GDP')
ax.legend()

fig8, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, np.log(Y))
ax.plot(year, np.log(Y_ss), 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel(r'$\ln(Y_t)$', rotation=0)
ax.set_title('simulated time path of log real GDP')
ax.legend()

fig9, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, wage)
ax.plot(year, wage_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel('wage')
ax.set_title('simulated time path of wage')
ax.legend()

fig10, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, rent)
ax.plot(year, rent_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel('rent')
ax.set_title('simulated time path of rent')
ax.legend()