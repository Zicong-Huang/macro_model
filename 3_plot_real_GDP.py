# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 08:26:11 2020

@author: Zicong Huang
"""
from fredapi import Fred
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter

fred = Fred()
rgdp = fred.get_series('GDPC1')
rec = fred.get_series('USREC', '1947-01-01')

#
# get recession starts and ends
def get_recession_start_end(dataframe):
    # series not begin in recession
    in_rec = 0
    rec_start = list()
    rec_end = list()
    rec_period = list()
    dates = rec.index
    for date in dates:
        if in_rec == 0 and dataframe[date] == 1:
            rec_start.append(date)
            in_rec = 1
        if in_rec == 1 and dataframe[date] == 0:
            rec_end.append(date)
            in_rec = 0
    
    for i in range(0, len(rec_end)):
        rec_period.append((rec_start[i],rec_end[i]))
    
    if len(rec_start) > len(rec_end):
        rec_period.append((rec_start[-1], dates[-1]))
        
    return rec_period

#
# plot real gdp 
fig1,ax = plt.subplots(figsize=(10,6), dpi = 300)
ax.plot(rgdp/1e3)
ax.set_xlabel('time')
ax.set_ylabel('trillions of chained 2012 dollars')
ax.set_title('US Real GDP, Quarterly')
# shade recession periods
rec_dates = get_recession_start_end(rec)
for pair in rec_dates:
    ax.axvspan(pair[0], pair[1], color='grey', alpha=0.3)
    
# apply hpfilter
cycle, trend = hpfilter(rgdp)

#
# plot real gdp with hpfilter
fig2,ax = plt.subplots(figsize=(10,6), dpi = 300)
ax.plot(rgdp/1e3)
ax.plot(trend/1e3, label = 'Hodrick–Prescott smoothing')
ax.set_xlabel('time')
ax.set_ylabel('trillions of chained 2012 dollars')
ax.set_title('US Real GDP, Quarterly')
ax.legend()
for pair in rec_dates:
    ax.axvspan(pair[0], pair[1], color='grey', alpha=0.3)

#
# log deviations from trend
log_cycle, log_trend = hpfilter(np.log(rgdp))
log_devia = np.log(rgdp) - log_trend

#
# plot log deviations
fig3,ax = plt.subplots(figsize=(10,6), dpi = 300)
ax.plot(log_devia*400) # why multiply by 400: annualize quarterly data
ax.set_title('Log Deviations of Quarterly Real GDP from its Trend')
ax.set_xlabel('time')
ax.set_ylabel('percentage deviation')
for pair in rec_dates:
    ax.axvspan(pair[0], pair[1], color='grey', alpha=0.3)

#
# log first difference
log_diff_gdp = np.log(rgdp) - np.log(rgdp.shift())

#
# plot log first difference
fig4, ax = plt.subplots(figsize=(10,6), dpi = 300)
ax.plot(log_diff_gdp*400)
plt.hlines(0, min(rgdp.index), max(rgdp.index), colors='red')
ax.set_title('Log First Difference of US Real GDP, Quarterly')
ax.set_xlabel('time')
ax.set_ylabel('first differences (in logs)')
for pair in rec_dates:
    ax.axvspan(pair[0], pair[1], color='grey', alpha=0.3)
    
