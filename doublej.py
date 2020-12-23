# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 14:30:00 2020

@author: jacob
"""

import numpy as np

def doublej(a1, b1):
    alpha0 = np.matrix(a1)
    gamma0 = np.matrix(b1)
    diff = 5
    timer = 1
    
    while diff > 1e-15:
        alpha1 = alpha0*alpha0
        gamma1 = gamma0 + alpha0*gamma0*alpha0.T
        diff = abs((gamma1 - gamma0)).max()
        alpha0 = alpha1
        gamma0 = gamma1
        timer += 1
        if timer > 100 or diff == np.Inf:
            raise TimeoutError('Not converging, check your inputs')
        
    return gamma1

'''
it can be checked that doublej is identitcal to singlej
'''

# a1 = [[0.1,0.2,0.7],
#       [0.3,0.3,0.4],
#       [0.6,0.2,0.2]]

# b1 = [[1,2,1],
#       [2,1,3],
#       [0,3,1]]

# v, timer = doublej(a1, b1)

# def singlej(a1, b1):
#     alpha0 = np.matrix(a1)
#     alpha1 = alpha0
#     gamma0 = np.matrix(b1)
#     diff = 5
#     timer = 1
    
#     while diff > 1e-15:
#         alpha1 = alpha1 * alpha0
#         gamma1 = gamma0 + alpha0*gamma0*alpha0.T
#         diff = abs((gamma1 - gamma0)).max()
#         alpha0 = alpha1
#         gamma0 = gamma1
#         timer += 1
#         if timer > 100 or diff == np.Inf:
#             raise TimeoutError('Not converging, check your inputs')
    
#     return gamma1, timer

# v2,timer2 = singlej(a1, b1)
        