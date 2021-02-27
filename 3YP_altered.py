#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3YP altered file.
Adapted from UoO EPG's energy management framework.
Authors: Avinash Vijay, Scot Wheeler, Mathew Hedges
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
pvInstallations = 1500
pv_site1 = AS.pvAsset(pvCapacity, pvInstallations)
non_dispatchable.append(pv_site1)

# Hydro Generation
hydroCapacity = 450 # this parameter is not actually used in this asset's object?
hydro_site1 = AS.hydroAsset(hydroCapacity)
non_dispatchable.append(hydro_site1)

# Load
nHouseholds = 1700
load_site1 = AS.loadAsset(nHouseholds) # domestic load
non_dispatchable.append(load_site1)

#load_site2 = AS.ndAsset()              # non-domestic load- waiting for minnie
#non_dispatchable.append(load_site2)

#load_site3 = AS.hpAsset()              # heat pump electricity demand- waiting for steven
#non_dispatchable.append(load_site3)

# Battery Storage
capacity = 36
power = 50 # fast charging power capacity
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
net_load, disp_load, non_disp_load = energy_system.basic_energy_balance()


#######################################
### STEP 6: setup and run the market
#######################################


# setup
grid_sale_price = 0.055       # price paid for exports (£/kWh) grid/Octopus
market1 = MK.marketObject(energy_system, export_rate= grid_sale_price) 

# run
opCost = market1.getTotalCost()
grid_cost = market1.getGridCost().sum()
print("Annual network cost: £ %.2f" % (grid_cost / 100))
purchased, sold = market1.gridBreakdown()

purchased_daily = ES.E_to_dailyE(purchased, dt) / 100  # convert to pounds
sold_daily = ES.E_to_dailyE(sold, dt) / 100            # convert to pounds


#######################################
### STEP 7: prepare lists for plotting
#######################################


pv_list1 = [i[0] for i in pv_site1.getOutput(dt).tolist()]           # plot pv generation 
hydro_list1 = [i[0] for i in hydro_site1.getOutput(dt).tolist()]     # plot hydro generation
load_list1 = [i[0] for i in load_site1.getOutput(dt).tolist()]       # plot domestic demand
#load_list2 = [i[0] for i in load_site2.getOutput(dt).tolist()]       # plot non-domestic demand
#load_list3 = [i[0] for i in load_site3.getOutput(dt).tolist()]       # plot heat pump electricity demand
battery_list1 = [i[0] for i in battery_site1.getOutput(net_load).tolist()] # domestic battery storage
battery_list2 = [i[0] for i in battery_site2.getOutput(net_load).tolist()] # community battery storage


#######################################
### STEP 8: plot results
#######################################


# plot data together, this only plots the 1st day in the year
fig,ax =  plt.subplots(nrows=4,ncols=2,sharex=True,sharey=False)
fig.tight_layout(pad=3.0)

x_axis = pd.date_range(datetime.datetime(2017,1,1), datetime.datetime(2017, 12, 31, 23, 59, 59), freq='0.5H')

ax[0][0].plot(x_axis[1:48], net_load[1:48])
ax[0][0].set_ylabel('Net Load, kWh')
ax[0][0].set_xlabel('Time')
ax[0][0].set_title('1')

ax[0][1].plot(x_axis[1:48], non_disp_load[1:48])
ax[0][1].set_ylabel('Net Non-dispatchable Load, kWh')
ax[0][1].set_xlabel('Time')
ax[0][1].set_title('2')

ax[1][0].plot(x_axis[1:48], disp_load[1:48])
ax[1][0].set_ylabel('Net Dispatchable, kWh')
ax[1][0].set_xlabel('Time')
ax[1][0].set_title('3')

ax[1][1].plot(x_axis[1:48], battery_list1[1:48])
ax[1][1].set_ylabel('Domestic Battery, kWh')
ax[1][1].set_xlabel('Time')
ax[1][1].set_title('4')

ax[2][0].plot(x_axis[1:48], load_list1[1:48])
ax[2][0].set_ylabel('Domestic Load, kWh')
ax[2][0].set_xlabel('Time')
ax[2][0].set_title('5')

ax[2][1].plot(x_axis[1:48], battery_list2[1:48])
ax[2][1].set_ylabel('Community Battery, kWh')
ax[2][1].set_xlabel('Time')
ax[2][1].set_title('6')

ax[3][0].plot(x_axis[1:48], pv_list1[1:48])
ax[3][0].set_ylabel('PV Generation, kWh')
ax[3][0].set_xlabel('Time')
ax[3][0].set_title('7')

ax[3][1].plot(x_axis[1:48], hydro_list1[1:48])
ax[3][1].set_ylabel('Hydro Generation, kWh')
ax[3][1].set_xlabel('Time')
ax[3][1].set_title('8')


plt.show()

# ignore
#print('mine')
#print(pd.date_range(start=datetime.datetime(year=2018,month=1,day=1,hour=0,minute=0), periods=48, freq='0.5H'))
#print('theirs')
#print(pd.date_range(datetime.datetime(2017,1,1), datetime.datetime(2017, 12, 31, 23, 59, 59), freq='0.5H'))