#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3YP altered file.
Adapted from UoO EPG's energy management framework.
Authors: Avinash Vijay, Scot Wheeler, Mathew Hedges,
Minnie Karanjavala, Ravi Kohli
"""

__version__ = '0.6'

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
import Emissions as EM


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

pvPanels = 180
pv_site2 = AS.sfAsset(pvCapacity, pvPanels)         # solar farm
non_dispatchable.append(pv_site2)


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


# Carbon Emissions Intensities
loss = 0.08 # 8% loss between generation and consumption of electricity
emission_intensity = EM.Emissions(loss)                                                     # numpy array gCO2/kWh
emission_intensity = [i[0] for i in emission_intensity.getEmissionIntensity().tolist()]     # list gCO2/kWh
emission_intensity = [i/1000000 for i in emission_intensity]                                   # list tnCO2/kWh
#print('carbon intensity of electricity consumption (list) coming...')
#print(emission_intensity)


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

sf = [i[0] for i in pv_site2.getOutput(dt).tolist()]                # average solar farm generation 
sf_means = AV.Averaging(sf)

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

gross_gen = [i+j+k for i,j,k in zip(hydro,pv,sf)]
gross_gen_means = AV.Averaging(gross_gen)


#######################################
### STEP 8: plot generation results
#######################################


# plotting style
plt.style.use('seaborn')

# 1st 5th of the year     # this is plotting average profiles found over the dates 1st Jan-14th March; the "Average.py" function finds these average profiles over this period
fig1 = PT.genPlotting(hydro_means[0], pv_means[0], sf_means[0], net_load_means[0], gross_gen_means[0], disp_load_means[0])
fig1.canvas.set_window_title('1st Jan - 14th Mar')

# 2nd 5th of the year
fig2 = PT.genPlotting(hydro_means[1], pv_means[1], sf_means[1], net_load_means[1], gross_gen_means[1], disp_load_means[1])
fig2.canvas.set_window_title('15th Mar - 26th May')

# 3rd 5th of the year
fig3 = PT.genPlotting(hydro_means[2], pv_means[2], sf_means[2], net_load_means[2], gross_gen_means[2], disp_load_means[2])
fig3.canvas.set_window_title('27th May - 7th Aug')

# 4th 5th of the year
fig4 = PT.genPlotting(hydro_means[3], pv_means[3], sf_means[3], net_load_means[3], gross_gen_means[3], disp_load_means[3])
fig4.canvas.set_window_title('8th Aug - 19th Oct')

# 5th 5th of the year
fig5 = PT.genPlotting(hydro_means[4], pv_means[4], sf_means[4], net_load_means[4], gross_gen_means[4], disp_load_means[4])
fig5.canvas.set_window_title('20th Oct - 31st Dec') 


#######################################
### STEP 9: plot load results
#######################################


# 1st 5th of the year     # this is plotting average profiles found over the dates 1st Jan-14th March; the "Average.py" function finds these average profiles over this period
Fig1 = PT.loadPlotting(net_load_means[0], non_disp_load_means[0], dom_means[0], nondom_means[0], None, None)#, ev_means[0], hp_means[0])
Fig1.canvas.set_window_title('1st Jan - 14th Mar')

# 2nd 5th of the year
Fig2 = PT.loadPlotting(net_load_means[1], non_disp_load_means[1], dom_means[1], nondom_means[1], None, None)#,ev_means[1], hp_means[1])
Fig2.canvas.set_window_title('15th Mar - 26th May')

# 3rd 5th of the year
Fig3 = PT.loadPlotting(net_load_means[2], non_disp_load_means[2], dom_means[2], nondom_means[2], None, None)#, ev_means[2], hp_means[2])
Fig3.canvas.set_window_title('27th May - 7th Aug')

# 4th 5th of the year
Fig4 = PT.loadPlotting(net_load_means[3], non_disp_load_means[3], dom_means[3], nondom_means[3], None, None)#, ev_means[3], hp_means[3])
Fig4.canvas.set_window_title('8th Aug - 19th Oct')

# 5th 5th of the year
Fig5 = PT.loadPlotting(net_load_means[4], non_disp_load_means[4], dom_means[4], nondom_means[4], None, None)#, ev_means[4], hp_means[4])
Fig5.canvas.set_window_title('20th Oct - 31st Dec') 


#######################################
### STEP 10: calculate and plot emissions
#######################################


# calculate CO2 emissions saved
x = emission_intensity                      # carbon emission intensities in tnCO2/kWh 
y = net_load                                # net load in kWh

emissions = []                              # emissions in tnCO2
for i,j in zip(x,y):
    if (i or j) == 'nan':                   # dealing with unruly nans - I don't know why there are so many???
        emissions.append(0)
    else:
        emission = i*j
        emissions.append(emission)

# plot the net emissions over 2020
fig,ax = plt.subplots()
plt.xticks(rotation=90)
fig.tight_layout(pad=3.0)

x_axis = pd.date_range('2020' + '-01-01', periods = 17520, freq= '0.5H') 
myFmt = mdates.DateFormatter('%H:%M')   # format the times into Hour:Minute format
plt.gcf().autofmt_xdate()               # automatic rotation of the axis plots

ax.plot(x_axis, emissions)
ax.set_ylabel('tnCO2')
ax.set_xlabel('Time')
ax.set_title('Net Emissions')
ax.xaxis.set_major_formatter(myFmt)     # apply HH:MM format to the x axis data
fig.canvas.set_window_title('1st Jan - 31st Dec')

"""
# plot the average emissions for a day in each quintile of the year 2020 - this is a mess!
emissions_means = AV.Averaging(emissions)
zero = np.zeros((48,1)).tolist()
fig6 = PT.Plotting(emissions_means[0], emissions_means[1], emissions_means[2], emissions_means[3], emissions_means[4], zero, zero, zero, zero)
fig6.canvas.set_window_title('Net Emissions Daily Mean of Each Quintile (incorrect labels, 4 are zeroed and 5 represent the quintile averages)')
"""

# find the net total emissions
emissions = ['{:.2f}'.format(i) for i in emissions]
print('Annual Net Emissions in tnCO2')
filtered = [float(element) for element in emissions if element != 'nan']
print(sum(filtered))


plt.show()