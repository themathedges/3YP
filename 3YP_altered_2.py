#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3YP altered file.
Adapted from UoO EPG's energy management framework.
Authors: Avinash Vijay, Scot Wheeler, Mathew Hedges,
Minnie Karanjavala, Ravi Kohli, Steven Jones
"""

__version__ = '0.4'

# import modules
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import Assets as AS
import EnergySystem as ES
import Market as MK
import Averaging as AV
import Plotting as PT


#######################################
### STEP 1: setup parameters
#######################################


dt = 30/60                # 30 minute time intervals
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
pv_site1 = AS.pvAsset(pvCapacity, pvInstallations) # domestic PV
non_dispatchable.append(pv_site1)

#pv_site2 = AS.sfAsset(pvCapacity, nPanels)         # solar farm
#non_dispatchable.append(pv_site2)


# Hydro Generation
hydroCapacity = 450 # this parameter is not actually used in this asset's object?
hydro_site1 = AS.hydroAsset(hydroCapacity)
non_dispatchable.append(hydro_site1)


# Loads
nHouseholds = 1728
load_site1 = AS.loadAsset(nHouseholds)   # domestic load
non_dispatchable.append(load_site1)

nBusinesses = 36
load_site2 = AS.ndAsset(nBusinesses)     # non-domestic load
non_dispatchable.append(load_site2)

#nCars = ?
#load_site3 = AS.ndAsset(nCars)           # EV electricity demand- waiting for Minnie 
#non_dispatchable.append(load_site3)

#load_site4 = AS.hpAsset(nHouseholds)     # heat pump electricity demand- waiting for steven
#non_dispatchable.append(load_site4)


# Battery Storage
capacity = 36
power = 50                                                                      # fast charging power capacity
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


# _means are lists of 5 nested lists, where each nested list is an averaged profile of over 1/5th of the year
net_load = [i[0] for i in net_load.tolist()]                        # average net load
net_load_means = AV.Averaging(net_load)

disp_load = [i[0] for i in disp_load.tolist()]                      # average net dispatchable load
disp_load_means = AV.Averaging(disp_load)                   

non_disp_load = [i[0] for i in non_disp_load.tolist()]              # average net non-dispatchable load
non_disp_load_means = AV.Averaging(non_disp_load)

pv = [i[0] for i in pv_site1.getOutput(dt).tolist()]                # average pv generation 
pv_means = AV.Averaging(pv)

#sf = [i[0] for i in pv_site2.getOutput(dt).tolist()]                # average solar farm generation 
#sf_means = AV.Averaging(sf)

hydro = [i[0] for i in hydro_site1.getOutput(dt).tolist()]          # average hydro generation
hydro_means = AV.Averaging(hydro)

dom = [i[0] for i in load_site1.getOutput(dt).tolist()]             # average domestic demand
dom_means = AV.Averaging(dom)

nondom = [i[0] for i in load_site2.getOutput(dt).tolist()]          # average non-domestic demand
nondom_means = AV.Averaging(nondom)

#ev = [i[0] for i in load_site3.getOutput(dt).tolist()]              # average EV electricity demand
#ev_means = AV.Averaging(ev)

#hp = [i[0] for i in load_site4.getOutput(dt).tolist()]              # average heat pump electricity demand
#hp_means = AV.Averaging(hp)

dombat = [i[0] for i in battery_site1.getOutput(net_load).tolist()] # average domestic battery storage
dombat_means = AV.Averaging(dombat)

combat = [i[0] for i in battery_site2.getOutput(net_load).tolist()] # average community battery storage
combat_means = AV.Averaging(combat)


#######################################
### STEP 8: plot results
#######################################


# 1st 5th of the year     # this is plotting average profiles found over the dates 1st Jan-14th March; the "Average.py" function finds these average profiles over this period
fig1 = PT.Plotting(net_load_means[0], disp_load_means[0], non_disp_load_means[0], pv_means[0], hydro_means[0], dom_means[0], nondom_means[0], dombat_means[0], combat_means[0])
fig1.canvas.set_window_title('1st Jan - 14th Mar')

# 2nd 5th of the year
fig2 = PT.Plotting(net_load_means[1], disp_load_means[1], non_disp_load_means[1], pv_means[1], hydro_means[1], dom_means[1], nondom_means[1], dombat_means[1], combat_means[1])
fig2.canvas.set_window_title('15th Mar - 26th May')

# 3rd 5th of the year
fig3 = PT.Plotting(net_load_means[2], disp_load_means[2], non_disp_load_means[2], pv_means[2], hydro_means[2], dom_means[2], nondom_means[2], dombat_means[2], combat_means[2])
fig3.canvas.set_window_title('27th May - 7th Aug')

# 4th 5th of the year
fig4 = PT.Plotting(net_load_means[3], disp_load_means[3], non_disp_load_means[3], pv_means[3], hydro_means[3], dom_means[3], nondom_means[3], dombat_means[3], combat_means[3])
fig4.canvas.set_window_title('8th Aug - 19th Oct')

# 5th 5th of the year
fig5 = PT.Plotting(net_load_means[4], disp_load_means[4], non_disp_load_means[4], pv_means[4], hydro_means[4], dom_means[4], nondom_means[4], dombat_means[4], combat_means[4])
fig5.canvas.set_window_title('20th Oct - 31st Dec') 


"""
## plot non-domestic profile <-- I can encorporate the non-dom profile into the subplot later. I just plotted it as a seperate figure here to check it was the correct shape
fig,ax = plt.subplots()
plt.xticks(rotation=90)
fig.tight_layout(pad=3.0)

x_axis = pd.date_range('2018' + '-01-01', periods = 48, freq= '0.5H') 
myFmt = mdates.DateFormatter('%H:%M')   # format the times into Hour:Minute format
plt.gcf().autofmt_xdate()               # automatic rotation of the axis plots

ax.plot(x_axis, nondom_means[0])
ax.set_ylabel('kWh')
ax.set_xlabel('Time')
ax.set_title('Non-Domestic Load')
ax.xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
fig.canvas.set_window_title('1st Jan - 14th Mar')
"""


plt.show()