# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 22:42:18 2020

@author: Zicong Huang

This program solves the following stochastic growth model:
    
    max E Sum_t beta*({c_t}^{1-sigma}-1)/(1-sigma)
    subject to:
        c_t + i_t = A_t*{k_t}^alpha
        k_{t+1} = (1-delta)*k_t + i_t
        A_t ~ markov{high, low}
        k_{t+1} >= 0
        c_t > 0
"""

import numpy as np
from markov import markov_chain

#
# set model parameters
alpha  = 0.40                        # capital share of income
beta   = 0.60                        # subjective discount factor
delta  = 0.50                        # 1 - depreciation rate
A_high = 1.25                        # high value for technology
A_low  = 0.50                        # low value for technology 
sigma  = 2.00                        # what is sigma?

prob   = np.array([                  # prob(i,j) = probability (A(t+1)=Aj|A(t)=Ai)
                  [0.8, 0.2],        #        high    low  ---- col: t+1
                  [0.2, 0.8]         # high [             ]
                  ])                 # low  [             ]---- row: t

#
# form capital grid
maxk =  25.01
inck =  0.01
mink =  0.01
nk   = round((maxk-mink)/inck)
kgrid = np.arange(mink, maxk, inck)        

#
# tabulate the utility function

kk  = np.array([kgrid]*nk)           # repeat array row-wise; k(t=1) increases along each row
kkp = np.array([kgrid]*nk).T         # repeat array col-wise; k(t=2) increases along each col

cons_high = A_high * (kk**alpha) + delta*kk - kkp       # consumption when tech shock is high
cons_low  = A_low  * (kk**alpha) + delta*kk - kkp       # consumption when tech shock is low

cons_high[cons_high<=0] = np.nan
cons_low[cons_low<=0] = np.nan

if sigma == 1:
    util_high = np.log(cons_high)
    util_low  = np.log(cons_low)
else:
    util_high = ((cons_high ** (1-sigma)) - 1)/(1-sigma)
    util_low  = ((cons_low  ** (1-sigma)) - 1)/(1-sigma)

util_high[np.isnan(util_high)] = -np.inf
util_low[np.isnan(util_low)]   = -np.inf

#
# initialize some variables
v = np.zeros((nk,2))          # first col: high; second col: low
decision = np.zeros((nk,2))   # first col: high; second col: low
test = 10

#
# iterate on Bellman's equation and get the decision rules and the value func
# at the optimum
while test > 1e-7:
    v_high = np.matmul(v, prob[0,])    # expected next period value given this period high
    v_low  = np.matmul(v, prob[1,])    # expected next period value given this period low
    bellman_high = util_high + beta*(np.array([v_high]*nk).T)  # value func given high shock this period
    bellman_low  = util_low  + beta*(np.array([v_low]*nk).T)   # value func given low shock this period
    
    tdecision_high = np.argmax(bellman_high, axis=0)    # given high shock, optimum decision
    tdecision_low  = np.argmax(bellman_low, axis=0)     # given low shock, optimum decision
    
    tv_high = np.max(bellman_high, axis=0)    # given high shock, maximized value
    tv_low = np.max(bellman_low, axis=0)      # given low shock, maximized value
    
    tdecision = np.array([tdecision_high, tdecision_low]).T
    tv = np.array([tv_high, tv_low]).T
    
    test = np.max(np.max(abs((tv-v)/v)))
    print(test)
    
    v = tv
    decision = tdecision


#
# form transition matrix
# trans is the transition matrix from state at t (row) to the state at t+1 (col)
# the eigenvector associated with the unit eigenvalue of trans' is the stationary
# distribution

g_high = np.zeros((nk,nk))
g_low = np.zeros((nk,nk))

for i in range(0,nk):
    g_high[i, tdecision_high[i]] = 1
    g_low[i, tdecision_low[i]] = 1
    
trans = np.vstack((np.hstack((prob[0,0]*g_high, prob[0,1]*g_high)),
                   np.hstack((prob[1,0]*g_low,  prob[1,1]*g_low))))
trans = trans.T

probst = (1/(2*nk))*np.ones((2*nk,1))
test = 1
while test > 1e-8:
    probst1 = np.matmul(trans, probst)
    test = max(abs(probst1-probst))
    probst = probst1
    print(test)


#
# vectorize the decision rule to be conformable with probst
# calculate mean level of capital
veck = decision.flatten('F')   # col major order
