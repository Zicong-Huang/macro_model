# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 19:39:51 2020

@author: zicong huang

deterministic growth model solved with dynamic programming

max \SUM_t beta^t ln c_t
s.t. c_t + k_{t+1} = exp(sigma) k_t ^ {alpha}

"""

import numpy as np
import matplotlib.pyplot as plt

#
# set model parameter
alpha = 0.35                        # capital share of income
beta = 0.90                         # subjective discounter
sigma = 0.40                        # TFP = exp(sigma)
A = np.exp(sigma)

#
# form capital grid
maxk = 1                            # maximum value of capital grid
inck = 0.001                        # size of capital grid increments
mink = 0 + inck                     # minimum value of capital grid
nk = round((maxk-mink)/inck+1)      # number of grid points
kgrid = np.arange(start = mink, stop = maxk+inck, step = inck)

''' Compute Analytical Solution '''
#
# compute the optimal value function from analytical solution v = v(kgrid)
optimal_value = (1/(1-beta))*(np.log(A*(1-beta*alpha))+((beta*alpha)/(1-beta*alpha))*np.log(A*beta*alpha))+(alpha/(1-alpha*beta))*np.log(kgrid)

#
# compute the optimal decision rule k' = f(k)
optimal_decision = alpha*beta*A*(kgrid**alpha)

#
# compute the steady state of the capital stock from analytical solution: k'=k for decision rule
k_ss = (alpha*beta*A)**(1/(1-alpha))       

''' numerical discrete solution '''
# tabulate the utility function such that for zero or negative consumption utility
# remains a large negative number so that such values will never be chosen as 
# utiilty maximizing

#
# prepare for k and k'
kk = np.array([kgrid]*nk)        # repeat array row-wise; k(t=1) increases along each row
kkp = np.array([kgrid]*nk).T     # repeat array col-wise; k(t=2) increases along each col

#
# impose budget constraint to get consumption
cons = A * (kk**alpha) - kkp

#
# rule out negative consumption
cons[cons<=0] = np.nan                        # for log utility, zero consumption is not valid

#
# log utility function
util = np.log(cons)

#
# if consumption is negative, set utility to negative infinity
util[np.isnan(util)] = -np.inf

#
# initialize some variables
test = 10
v = -1 * np.ones(nk)
decision = np.zeros(nk)
nrow, ncol = util.shape

#
# iterate on bellman's equation and get the decision rules and the value func
# at the optimum
while test > 1e-10:
    # get updated value function and best decision
    bellman = util + beta*(np.array([v]*nk).T)
    tdecision = np.argmax(bellman,axis=0)
    tv = np.max(bellman,axis=0)
    
    test = np.max(abs((tv - v)/v))
    
    v = tv
    decision = tdecision

decision = mink + tdecision * inck

#
# plots
fig1, ax = plt.subplots(figsize=(10,6), dpi = 300)
ax.plot(kgrid, decision)
ax.plot(kgrid, kgrid, label = r'$45^{\circ}$ line')
ax.plot(k_ss,k_ss,'ro', label = 'steady state rate')
plt.xlim((0,1))
plt.ylim((0,1))
ax.set_title("decision rules for saving rate: deterministic dynamic programming")
ax.set_xlabel('capital this period')
ax.set_ylabel('capital next period')
plt.legend()

fig2, ax = plt.subplots(figsize=(10,6), dpi = 300)
ax.plot(kgrid, v)
plt.xlim(xmin = 0)
ylow, yhigh = ax.get_ylim()
plt.ylim(ymin = ylow)
ax.vlines(k_ss, ylow, yhigh, label = 'steady state', color = 'red')
ax.set_title('optimized value function: deterministic dynamic programming')
ax.set_xlabel('capital stock')
ax.set_ylabel('value function')
plt.legend()
