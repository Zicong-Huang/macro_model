# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 19:39:51 2020

@author: zicong huang

deterministic growth model solved with dynamic programming

max \SUM_t beta^t ln c_t
s.t. c_t + k_{t+1} = exp(sigma) k_t ^ {alpha}
"""

import numpy as np

#
# set model parameter
alpha = 0.30                        # capital share of income
beta = 0.80                         # subjective discounter
sigma = 0.20                        # TFP = exp(sigma)
A = np.exp(sigma)

#
# form capital grid
maxk = 1                            # maximum value of capital grid
inck = 0.001                        # size of capital grid increments
mink = 0                            # minimum value of capital grid
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
k_2 = np.array([kgrid]*nk)                    # repeat array col-wise
k_1 = np.array([kgrid]*nk).T                  # repeat array row-wise

#
# impose budget constraint to get consumption
cons = A * (k_1**alpha) - k_2

#
# rule out negative consumption
cons[cons<=0] = np.nan                        # for log utility, zero consumption is not valid

#
# log utility function
util = np.log(cons)

#
# if consumption is negative, set utility to negative infinity
util[np.isnan(cons)] = -np.inf

#
# initialize some variables
iter = 0
v = -76*np.ones(nk)    #???
decision = np.zeros(nk)
test = 10
nrow, ncol = util.shape

#
# iterate on bellman's equation and get the decision rules and the value func
# at the optimum

while test > 1e-7:
    # get updated value function and best decision
    bellman = util + beta*(np.array([v]*nk).T)
    tdecision = np.argmax(bellman,axis=0) # max argument for each rows
    tv = np.max(bellman,axis=0)           # max for each rows
    
    test = np.max(abs((tv - v)/v))          # marginal change of value for each iteration
    print(test)
    
    v = tv
    decision = tdecision


#
# decision is computed numerically
decision = decision*inck + mink
