# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 21:50:48 2020

@author: jacob
"""
import numpy as np

def markov_chain(T, n=200, s0=0, V=None):
    '''
    generates a simulation from a Markov chain of dimension the size of T

    Parameters
    ----------
    T : array-like object
        transition matrix
    n : int
        number of periods to simulate
    s0 : int
        position of the initial state
    V : vector
        quantitive corresponding to each state

    Returns
    -------
    chain, state
    chain: simulated markov chain
    state: simulated state vectors
    '''
    T = np.array(T)
    # check if T is square matrix
    row,col = T.shape
    if row != col:
        raise ValueError('Transition matrix should be squared')
    # check if T has more than 1 dims
    if row < 2:
        raise ValueError('Transition matrix must have more than 2 dimensions')
    # check if all elements numeric
    try:
        rowsum = np.sum(T, axis=1)
    except TypeError:
        raise TypeError('Transition matrix contains numeric elements only')
    # check if rowwise summation are 1
    if not np.all(rowsum == 1):
        raise ValueError('Each row of the transition matrix must sum to 1')
    
    x = np.random.rand(n)
    s = np.zeros(row)
    s[s0] = 1
    cum_prob = T.dot(np.triu(np.ones(T.shape)))
    
    state = np.array([0,0,0])
    
    for k in range(0, n):
        state = np.c_[state, s]
        conditional_cum_prob = s.dot(cum_prob)
        conditional_cum_prob = np.insert(conditional_cum_prob,0,0)
        weakly_less = np.array([x[k]<=z for z in conditional_cum_prob[1:]])
        strict_greater = np.array([x[k]>z for z in conditional_cum_prob[:-1]])
        s = weakly_less * strict_greater * 1
    
    V = np.array(V)
    state = state[:,1:]
    chain = V.dot(state)
    
    return chain, state
        
        


