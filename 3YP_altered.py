# -*- coding: utf-8 -*-

"""
3YP altered file.
Adapted from UoO EPG's energy management framework.
Authors: Avinash Vijay, Scot Wheeler
"""

__version__ = '0.4'

# import modules

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import datetime
from pandas import Timestamp

import Assets as AS
import EnergySystem as ES
import Market as MK


#######################################
### STEP 1: setup parameters
#######################################

dt = 30/60  # 30 minute time intervals
T = int((24 * 365) / dt)  # Number of intervals per year

#######################################
### STEP 2: setup the assets
#######################################

dispatchable = []
non_dispatchable = []
all_assets = []

# PV Generation
pvCapacity = 4
pvInstallations = 10000#1500
pv_site1 = AS.pvAsset(pvCapacity, pvInstallations)
non_dispatchable.append(pv_site1)

# Hydro Generation
hydroCapacity = 450
hydro_site1 = AS.hydroAsset(hydroCapacity)
non_dispatchable.append(hydro_site1)

# Load
nHouseholds = 1700
load_site1 = AS.loadAsset(nHouseholds) # domestic load
non_dispatchable.append(load_site1)

#load_site2 = AS.ndAsset() # non-domestic load
#non_dispatchable.append(load_site2)

#load_site3 = AS.hpAsset() # heat pump electricity demand
#non_dispatchable.append(load_site3)

# Battery Storage
capacity = 36
power = 50#6.6
eff = 0.7
nUsers1 = 700
nUsers2 = 200
battery_site1 = AS.PracticalBatteryAsset1(dt, T, capacity, power, eff, nUsers1) # domestic battery storage - 1st life EVs
dispatchable.append(battery_site1)
battery_site2 = AS.PracticalBatteryAsset2(dt, T, capacity, power, eff, nUsers2) # community battery storage - 2nd life EVs
dispatchable.append(battery_site2)

#######################################
#STEP 4: setup and run the energy system
#######################################

all_assets = non_dispatchable + dispatchable

# setup
energy_system = ES.EnergySystem(non_dispatchable, dispatchable, dt, T)
# run
net_load, disp_load, non_disp_load= energy_system.basic_energy_balance()

#######################################
### STEP 6: setup and run the market
#######################################

grid_sale_price = 0.055       # price paid for exports (£/kWh) grid/Octopus
market1 = MK.marketObject(energy_system, export_rate= grid_sale_price) 

# run
opCost = market1.getTotalCost()
grid_cost = market1.getGridCost().sum()
print("Annual network cost: £ %.2f" % (grid_cost / 100))
purchased, sold = market1.gridBreakdown()

purchased_daily = ES.E_to_dailyE(purchased, dt) / 100  # convert to pounds
sold_daily = ES.E_to_dailyE(sold, dt) / 100            # convert to pounds

# #######################################
# ### STEP 7: plot results
# #######################################

# plot data together
fig,ax =  plt.subplots(nrows=3,ncols=2,sharex=True,sharey=False)
fig.tight_layout(pad=3.0)

x_axis = pd.date_range(datetime.datetime(2017,1,1), datetime.datetime(2017, 12, 31, 23, 59, 59), freq='0.5H')

ax[0][0].plot(x_axis[1:48], net_load[1:48])
ax[0][0].set_ylabel('Net Load')
ax[0][0].set_xlabel('Time')
ax[0][0].set_title('1')

ax[0][1].plot(x_axis[1:48], non_disp_load[1:48])
ax[0][1].set_ylabel('Net Non-dispatchable Load')
#ax[0][1].set_ylabel('Domestic Load')
ax[0][1].set_xlabel('Time')
ax[0][1].set_title('2')

ax[1][0].plot(x_axis[1:48], disp_load[1:48])
ax[1][0].set_ylabel('Net Dispatchable')
#ax[1][0].set_ylabel('PV Generation')
ax[1][0].set_xlabel('Time')
ax[1][0].set_title('3')

#ax[1][1].plot(battery_site2.output.T)
#ax[1][1].set_ylabel('Non-domestic Load')
ax[1][1].set_xlabel('Time')
ax[1][1].set_title('4')

#ax[0][2].plot(pv_site1.output.T)
#ax[2][0].set_ylabel('Hydro Generation')
ax[2][0].set_xlabel('Time')
ax[2][0].set_title('6')

#ax[1][2].plot(all_assets)
#ax[2][1].set_ylabel('Heat Pump Load')
ax[2][1].set_xlabel('Time')
ax[2][1].set_title('6')

#print('mine')
#print(pd.date_range(start=datetime.datetime(year=2018,month=1,day=1,hour=0,minute=0), periods=48, freq='0.5H'))
#print('theirs')
#print(pd.date_range(datetime.datetime(2017,1,1), datetime.datetime(2017, 12, 31, 23, 59, 59), freq='0.5H'))
plt.show()