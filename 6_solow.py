# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 15:36:08 2020

@author: Zicong Huang

This program simulate a baseline solow model
"""
import numpy as np
import matplotlib.pyplot as plt
#
# set initial value for K, N, Y
K0 = 300       # capital stock
Y0 = 600       # real GDP
N0 = 5         # population

#
# set values for parameters of the model
alpha = 0.5               # capital share of income
delta = 0.10            # depreciation rate of capital
s = 0.20                # saving rate
n = 0.01               # population growth rate
T = 100               # number of periods to simulate
start_year = 2000

#
# initial level of A
A0 = Y0/((K0**alpha)*(N0**(1-alpha)))

#
# initialize time series
# compute initial capital-to-labor ratio
K_N = np.zeros(T)        # capital-to-labor ratio
N = np.zeros(T)          
K_N[0] = K0/N0
N[0] = N0
A = np.ones(T)*A0        # Solow residuals not changed

#
# simulate model
for t in range(0, T-1):
    N[t+1] = (1 + n) * N[t]
    K_N[t+1] = ((1-delta)*K_N[t])/(1+n) + (s*A[t]*(K_N[t] ** alpha))/(1+n)

#
# compute output per worker, total capital, total output, wages and rental rate
# of capital
Y_N = A * K_N ** alpha
K = K_N * N
Y = A * (K ** alpha) * (N ** (1-alpha))
rental_rate = alpha * A * (K ** (alpha-1)) * (N ** (1-alpha))
wages = (1-alpha) * A * (K ** (alpha)) * (N ** (-alpha))

#
# steady state
K_N_ss = (s*A/(n + delta))**(1/(1-alpha))
Y_N_ss = A * K_N_ss ** (alpha)
K_ss = K_N_ss * N
Y_ss = A * (K_ss ** alpha) * (N ** (1-alpha))
wage_ss = (1-alpha) * A * (K_ss ** (alpha)) * (N ** (-alpha))
rent_ss = alpha * A * (K_ss ** (alpha-1)) * (N ** (1-alpha))

#
# growth rate log first difference
Y_growth = np.log(Y[1:]) - np.log(Y[:-1])


#
# steady state growth
Y_ss_growth = np.log(Y_ss[1:]) - np.log(Y_ss[:-1])

#
# solow diagram 1
TT = 800
kk = np.arange(0, TT)
outflow = (n + delta) * kk
inflow = s * A0 * kk ** alpha
output_pc = A0 * kk ** alpha

kk_ss = np.argwhere(np.diff(np.sign(inflow - outflow))).flatten() # find intersection: steady state

#
# solow diagram 2
kk_t1 = np.arange(0, TT)
kk_t2 = np.zeros(TT)
for t in range(0,TT):
    kk_t2[t] = ((1-delta)*kk_t1[t])/(1+n) + (s*A0*(kk_t1[t] ** alpha))/(1+n)

kk_ss2 = np.argwhere(np.diff(np.sign(kk_t2 - kk_t1))).flatten() # find intersection: steady state


#
# plottings
year = np.arange(start_year,start_year+T)

fig0, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(kk, inflow, label = r'$sf(k)$')
ax.plot(kk, output_pc, label = r'$f(k)$')
ax.plot(kk, outflow, label = r'($n+\delta)k$')
if len(kk_ss) == 2:
    kk_ss = kk_ss[1]
    inflow_ss = inflow[kk_ss]
    output_pc_ss = output_pc[kk_ss]
    
    ax.vlines(kk_ss, 0, output_pc_ss, linestyles = 'dotted', colors = 'black')
    ax.hlines(inflow_ss, 0, kk_ss, linestyles = 'dotted', colors = 'black')
    ax.hlines(output_pc_ss, 0, kk_ss, linestyles = 'dotted', colors = 'black')
ax.set_xlim(xmin = 0)
ax.set_ylim(ymin = 0)
ax.legend()
ax.set_xlabel(r'$k$')
ax.set_ylabel('values')
ax.set_title('solow diagram 1')


motion = r'$k_{t+1}=\frac{(1-\delta)}{1+n} \times k_{t} + \frac{s \times A}{1+n} \times k_{t}^\alpha $'
fig1, ax = plt.subplots(figsize = (10,6), dpi = 300)
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
ax.legend(prop={'size': 15})
ax.set_xlabel(r'$k_{t}$')
ax.set_ylabel(r'$k_{t+1}$')
ax.set_title('solow diagram 2')


fig2, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year ,K_N)
ax.set_xlabel('Year')
ax.set_ylabel('capital-to-labor')
ax.set_title('simulated path of the capital-to-labor ratio')
plt.hlines(K_N_ss, min(year), max(year), colors='red', linestyles='--',label = 'steady state')
plt.xticks(year[::10])
ax.legend(loc = 4)

fig3, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y_N)
ax.set_xlabel('Year')
ax.set_ylabel('output-per-worker')
ax.set_title('simulated time path of real GDP per worker')
plt.hlines(Y_N_ss, min(year), max(year), colors='red', linestyles='--',label = 'steady state')
plt.xticks(year[::10])
ax.legend(loc = 4)

fig4, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, wages)
ax.set_xlabel('Year')
ax.set_ylabel('wages')
ax.set_title('simulated time path of real wage')
plt.hlines(wage_ss, min(year), max(year), colors='red', linestyles='--',label = 'steady state')
plt.xticks(year[::10])
ax.legend(loc = 4)

fig5, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, rental_rate)
ax.set_xlabel('Year')
ax.set_ylabel('rental rate of capital')
ax.set_title('simulated time path of real rental rate')
plt.hlines(rent_ss, min(year), max(year), colors='red', linestyles='--',label = 'steady state')
plt.xticks(year[::10])
ax.legend(loc = 1)

fig6, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y)
ax.plot(year, Y_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel('output')
ax.set_title('simulated time path of real GDP')
plt.xticks(year[::10])
ax.legend(loc = 0)

fig7, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K)
ax.plot(year, K_ss, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel('capital')
ax.set_title('simulated time path of capital stock')
plt.xticks(year[::10])
ax.legend(loc = 0)

fig8, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, np.log(Y))
ax.plot(year, np.log(Y_ss), 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel('log output')
ax.set_title('simulated time path of log real GDP')
plt.xticks(year[::10])
ax.legend(loc = 0)

fig9, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year[1:], Y_growth * 100)
ax.plot(year[1:], Y_ss_growth * 100, 'r--', label = 'steady state')
ax.set_xlabel('Year')
ax.set_ylabel('percentage growth rate')
ax.set_title('simulated time path of real GDP growth')
plt.hlines(0, min(year), max(year), colors='black')
plt.xticks(year[::10])
ax.legend(loc = 0)


