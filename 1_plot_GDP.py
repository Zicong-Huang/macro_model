# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 01:41:35 2020

This program plots US GDP

@author: Zicong Huang
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

#
# load GDP data
gdp_data = pd.read_excel('USGDP_1790-2019.xlsx', header=1)

#
# extract column values
varnames = list(gdp_data)
year = gdp_data[varnames[0]]
nominal_gdp = gdp_data[varnames[1]]*1e6
real_gdp = gdp_data[varnames[2]]*1e6
gdp_deflator = gdp_data[varnames[3]]
pop = gdp_data[varnames[4]]*1e3
nominal_gdp_pc = gdp_data[varnames[5]]
real_gdp_pc = gdp_data[varnames[6]]

#
# plot nominal GDP
fig1, ax = plt.subplots(figsize = (10,6), dpi=300)
ax.plot(year, nominal_gdp/1e12)
ax.set_title('US Nominal GDP from 1790 to 2019')
ax.set_xlabel('year')
ax.set_ylabel('trillions of nominal dollars')
plt.xticks(year[::20])

#
# plot gdp deflator
fig2, ax = plt.subplots(figsize = (10,6),dpi=300)
ax.plot(year, gdp_deflator)
ax.set_xlabel('year')
ax.set_ylabel('GDP price deflator (2012 = 100)')
ax.set_title('US GDP deflator from 1790 to 2019')
ax.annotate('Great Depression', xy=(1929, gdp_deflator[year==1929]), 
            xytext=(1929, 40), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('Civil War', xy=(1864, gdp_deflator[year==1864]), 
            xytext=(1864, 40), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('World War I', xy=(1916, gdp_deflator[year==1918]), 
            xytext=(1890, 20), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
plt.xticks(year[::20])

#
# plot log base10 gdp deflator
fig3, ax = plt.subplots(figsize = (10,6),dpi=300)
ax.plot(year, gdp_deflator)
ax.set_xlabel('year')
ax.set_ylabel('base 10 log of GDP price deflator (2012 = log(100))')
ax.set_title('US GDP deflator, log of, base 10')
ax.annotate('Great Depression', xy=(1929, gdp_deflator[year==1929]), 
            xytext=(1929, 40), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('Civil War', xy=(1864, gdp_deflator[year==1864]), 
            xytext=(1864, 40), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('World War I', xy=(1916, gdp_deflator[year==1918]), 
            xytext=(1890, 20), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
ax.set_yscale('log', basey = 10)
plt.xticks(year[::20])

#
# plot gdp deflator natural log of
fig4, ax = plt.subplots(figsize = (10,6),dpi=300)
ax.plot(year, np.log(gdp_deflator))
ax.set_xlabel('year')
ax.set_ylabel('ln of GDP price deflator (2012 = log(100))')
ax.set_title('US GDP deflator, ln of')
ax.annotate('Great Depression', xy=(1929, np.log(gdp_deflator)[year==1929]), 
            xytext=(1929, 3), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('Civil War', xy=(1864, np.log(gdp_deflator)[year==1864]), 
            xytext=(1864, 3), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('World War I', xy=(1916, np.log(gdp_deflator)[year==1918]), 
            xytext=(1890, 3), fontsize = 10,
            arrowprops=dict(arrowstyle = '->'))
plt.xticks(year[::20])

#
# plot inflation
inflation = np.log(gdp_deflator) - np.log(gdp_deflator.shift(1))
mean_infla = np.mean(inflation)

fig5, ax = plt.subplots(figsize = (10,6),dpi=300)
ax.plot(year, inflation)
ax.set_xlabel('year')
ax.set_ylabel('annual inflation rate')
ax.set_title('US inflation rate, %')
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(1, decimals=0))
plt.xticks(year[::20])
plt.hlines(mean_infla, min(year), max(year), colors='red', linestyles='dashed')
plt.hlines(0, min(year), max(year), colors='aquamarine', linestyles='dotted')
ax.annotate('war of 1812', xy=(1813, 0.15),
            xytext=(1830, 0.15), fontsize=10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('civil war', xy=(1865, 0.15),
            xytext=(1880, 0.15), fontsize=10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('WWI', xy=(1918, 0.15),
            xytext=(1933, 0.15), fontsize=10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('WWI', xy=(1934, -0.1),
            xytext=(1950, -0.1), fontsize=10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('end of WWII price control', xy=(1950, 0.1),
            xytext=(1960, 0.15), fontsize=10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('1970 inflation', xy=(1975, 0.04),
            xytext=(1975, -0.05), fontsize=10,
            arrowprops=dict(arrowstyle = '->'))
ax.annotate('mean: 1.44%', xy=(1870, 0.015),
            xytext=(1870, 0.05), fontsize=10,
            arrowprops=dict(arrowstyle = '->'))

#
# plot US real GDP
fig6, ax = plt.subplots(figsize = (10,6),dpi=300)
ax.plot(year, real_gdp/1e12)
ax.set_xlabel('year')
ax.set_ylabel('trillions of 2012 dollars')
ax.set_title('US Nominal GDP from 1790 to 2019')
plt.xticks(year[::20])
