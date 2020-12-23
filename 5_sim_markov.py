# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 21:50:30 2020

@author: zicong huang
"""

from markov import markov_chain
import numpy as np
import matplotlib.pyplot as plt

transition = np.array(
             [[0.1, 0.5, 0.3, 0.1],
              [0.4, 0.2, 0.1, 0.3],
              [0.2, 0.3, 0.2, 0.3],
              [0.5, 0.2, 0.1, 0.2]])
n = 100
s0 = 2
V = [-1,0,1,2]
chain, state = markov_chain(transition, n, s0, V)

fig,ax = plt.subplots(figsize = (10,6), dpi = 300)
ax.plot(chain)
ax.set_title('sim: markov chain')
ax.set_xlabel('time')
ax.set_ylabel('value')
