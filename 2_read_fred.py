# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 08:22:36 2020

@author: Zicong Huang
"""

from fredapi import Fred
import matplotlib.pyplot as plt

# need add fred api to environment variable
fred = Fred()

#
# plot nominal gdp
gdp = fred.get_series('GDP') # Billions of Dollars, Seasonally Adjusted Annual Rate
gdp = gdp.dropna()           # drop missing values

fig1, ax = plt.subplots(figsize=(10,6), dpi=300)
ax.plot(gdp)
ax.set_xlabel('time')
ax.set_ylabel('billions of Nominal Dollars')
ax.set_title('US nominal GDP from FRED, quarterly')
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()]) # use , as thousand separator

#
# plot initial claims
ICSA = fred.get_series('ICSA') # weekly, seasonally adjusted, initial claim of unemployment

fig2, ax = plt.subplots(figsize=(10,6), dpi=300)
ax.plot(ICSA/1e6)
ax.set_xlabel('time')
ax.set_ylabel('millions of claims')
ax.set_title('weekly initial claim of unemployment, seasonally adjusted')