# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 06:13:06 2020

@author: zicong huang

This program simulate a solow model with human capital
"""
import numpy as np
import matplotlib.pyplot as plt

# initial inputs
K0 = 5
H0 = 3
E0 = 1
N0 = 8
A = 7

# set model parameters
alpha = 0.26            # physical capital income share of output
beta = 0.10             # human capital income share of output
gamma = 1-alpha-beta    # effective labor income share of output
delta_k = 0.08            # depreciation rate of physical capital
delta_h = 0.04         # depreciation rate of human capital
n = 0.0015              # population growth rate
g = 0.01               # labor-aug technology growth rate
sk = 0.20               # saving rate of physical capital
sh = 0.10               # saving rate of human capital
T = 150                 # periods simulated
start_year = 2000

# initial GDP
Y0 = A * (K0**alpha) * (H0**beta) * ((E0*N0)**gamma)

# initialize time series
K_EN = np.zeros(T)
H_EN = np.zeros(T)
E = np.zeros(T)
N = np.zeros(T)
EN = np.zeros(T)

K_EN[0] = K0/(E0*N0)
H_EN[0] = H0/(E0*N0)
E[0] = E0
N[0] = N0
EN[0] = E0*N0

# simulate the model
for t in range(0,T-1):
    K_EN[t+1] = ((1-delta_k)/((1+g)*(1+n)))*K_EN[t] + ((sk*A)/((1+g)*(1+n)))*(K_EN[t]**alpha)*(H_EN[t]**beta)
    H_EN[t+1] = ((1-delta_h)/((1+g)*(1+n)))*H_EN[t] + ((sh*A)/((1+g)*(1+n)))*(K_EN[t]**alpha)*(H_EN[t]**beta)
    E[t+1] = (1+g) * E[t]
    N[t+1] = (1+n) * N[t]
    
EN = E*N

# compute a bunch of values
Y_EN = A * (K_EN**alpha) * (H_EN**beta)
K_N = K_EN*E
H_N = H_EN*E
K = K_N * N
H = H_N * N
Y_N = Y_EN*E
Y = Y_N * N
wage = gamma * A * (K**alpha) * (H**beta) * (E**gamma) * (N**(gamma-1))
rent_k = alpha * A * (K**(alpha-1)) * (H**beta) * ((E*N) ** gamma)
rent_h = beta * A * (K**alpha) * (H**(beta-1)) * ((E*N) ** gamma)


# steady state
K_EN_ss = ((((sk*A)/(n+g+delta_k))**(1-beta)) * (((sh*A)/(n+g+delta_h))**beta))**(1/gamma)
H_EN_ss = ((((sk*A)/(n+g+delta_k))**(alpha)) * (((sh*A)/(n+g+delta_h))**(1-alpha)))**(1/gamma)
K_N_ss = K_EN_ss*E
H_N_ss = H_EN_ss*E
K_ss = K_N_ss * N
H_ss = H_N_ss * N
Y_EN_ss = A * (K_EN_ss**alpha) * (H_EN_ss**beta)
Y_N_ss = Y_EN_ss * E
Y_ss = Y_N_ss * N

wage_ss = gamma * A * (K_ss**alpha) * (H_ss**beta) * (E**gamma) * (N**(gamma-1))
rent_k_ss = alpha * A * (K_ss**(alpha-1)) * (H_ss**beta) * ((E*N) ** gamma)
rent_h_ss = beta * A * (K_ss**alpha) * (H_ss**(beta-1)) * ((E*N) ** gamma)

# plots
year = np.arange(start_year, start_year + T)

fig1, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K_EN, label = 'physical capital')
ax.plot(year, H_EN, label = 'human capital')
ax.hlines(K_EN_ss, min(year), max(year), linestyles = 'dashed', colors = 'red')
ax.hlines(H_EN_ss, min(year), max(year), linestyles = 'dashed', colors = 'red')
ax.set_xlabel('year')
ax.set_ylabel('stock per effective labor')
ax.set_title('simulated time path of capital per effective labor')
ax.legend()

fig2, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K_N, label = 'physical capital')
ax.plot(year, H_N, label = 'human capital')
ax.plot(year, K_N_ss, 'r--')
ax.plot(year, H_N_ss, 'r--')
ax.set_xlabel('Year')
ax.set_ylabel('capital-to-labor')
ax.set_title('simulated time path of capital to labor')
ax.legend()

fig3, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, K, label = 'physical capital')
ax.plot(year, H, label = 'human capital')
ax.plot(year, K_ss, 'r--')
ax.plot(year, H_ss, 'r--')
ax.set_xlabel('Year')
ax.set_ylabel('capital stock')
ax.set_title('simulated time path of capital stock')
ax.legend()

fig4, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y_EN)
ax.hlines(Y_EN_ss, min(year), max(year), linestyles = 'dashed', colors = 'red')
ax.set_xlabel('Year')
ax.set_ylabel('output per effective labor')
ax.set_title('simulated time path of output to effective labor')

fig5, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y_N)
ax.plot(year, Y_N_ss, 'r--')
ax.set_xlabel('Year')
ax.set_ylabel('output per worker')
ax.set_title('simulated time path of output to labor')

fig6, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, Y)
ax.plot(year, Y_ss, 'r--')
ax.set_xlabel('Year')
ax.set_ylabel('output')
ax.set_title('simulated time path of real GDP')

fig7, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, np.log(Y))
ax.plot(year, np.log(Y_ss), 'r--')
ax.set_xlabel('Year')
ax.set_ylabel('log output')
ax.set_title('simulated time path of log real GDP')

fig8, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, wage)
ax.plot(year, wage_ss, 'r--')
ax.set_xlabel('Year')
ax.set_ylabel('wage')
ax.set_title('simulated time path real wage')


fig9, ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(year, rent_k, label = 'return to physical capital')
ax.plot(year, rent_h, label = 'return to human capital')
ax.plot(year, rent_k_ss, 'r--')
ax.plot(year, rent_h_ss, 'r--')
ax.set_xlabel('Year')
ax.set_ylabel('return')
ax.set_title('simulated time path of real return to capital')
ax.legend()