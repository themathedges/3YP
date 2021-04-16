#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3YP Standalone Kennington Energy System (c. 2020) main file.
Adapted from UoO EPG's energy management framework.
Authors: Avinash Vijay, Scot Wheeler, Mathew Hedges,
Minnie Karanjavala, Ravi Kohli, Steven Jones
"""

__version__ = '0.7'

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
# Domestic Solar PV
dom_pvCapacity = 4                                                              # 4 kW domestic PV installations
annual_degradation = 0                                                          # solar panels at max efficiency upon installation
nInstallations = 0.028*1985                                                     # 2.8% of households currently have domestic PV
pv_site1 = AS.pvAsset(dom_pvCapacity, nInstallations)                      
non_dispatchable.append(pv_site1)

# Solar PV Farm
sf_pvCapacity = 0.45                                                            # 450 W PV panels
nPanels = 40000                                                                 # 35,000 panel solar farm
pv_site2 = AS.sfAsset(sf_pvCapacity, nPanels, annual_degradation)          
non_dispatchable.append(pv_site2)


# Hydro Generation
hydro_dataset = 'data/Sandford_hydro_generation_30_min_date.csv'
hydroCapacity = 450                                                             
hydro_site1 = AS.hydroAsset(hydroCapacity, hydro_dataset)
non_dispatchable.append(hydro_site1)


# Loads
# Domestic Load
domestic_dataset = 'data/ken_dom_annual_demand_per_household_3.csv'
nHouseholds = 1985                                                              # households in Kennington
load_site1 = AS.loadAsset(nHouseholds, domestic_dataset)   
non_dispatchable.append(load_site1)

# Non-Domestic Load
nondomestic_dataset = 'data/ken_non_dom_annual_demand_per_user_3.csv'
nBusinesses = 32                                                                # businesses in Kennington: 36 in total including schools
load_site2 = AS.ndAsset(nBusinesses, nondomestic_dataset)    
non_dispatchable.append(load_site2)

# School Load
school_dataset = 'data/school_annual_demand.csv'
nSchools = 2                                                                    # schools in Kennington: 2 full size primary schools and 2 small nurseries (we assume the demand of the nurseries has been covered in this school profile) 
load_site7 = AS.ndAsset(nSchools, school_dataset)
non_dispatchable.append(load_site7)


# 2050 EV Car Figures
total_nCars = 67                      # total num of EVs in 2020 (ICEs won't be adding load to the system)
percentage_night_charge = 1        # % of total cars which are charging at night in Ken

# EV Night Charging Load
night_dataset = 'data/EV_Demand_night_1.csv'
nCars_night = percentage_night_charge*total_nCars
load_site9 = AS.evAsset(nCars_night, night_dataset)
non_dispatchable.append(load_site9)

# EV Day Charging Load
day_dataset = 'data/EV_Demand_day_1.csv'
nCars_day = total_nCars-nCars_night                                                                     # EVs in Kennington
load_site3 = AS.evAsset(nCars_day, day_dataset)            
non_dispatchable.append(load_site3)


# Central Heat Pump Electricity Load  
central_dataset = 'data/centralheatpump.csv'  
nPumps = 1
load_site4 = AS.hpAsset(nPumps, central_dataset)    
non_dispatchable.append(load_site4)

# Shoebox Heat Pumps Load
domestic_shoebox_dataset = 'data/domestic_demand.csv'
nondomestic_shoebox_dataset = 'data/nondomestic_demand.csv'
load_site5 = AS.hpAsset(nHouseholds, domestic_shoebox_dataset)                 # domestic shoebox heat pumps
load_site6 = AS.hpAsset(nPumps, nondomestic_shoebox_dataset)                   # non-domestic shoebox heat pumps
non_dispatchable.append(load_site5) 
non_dispatchable.append(load_site6) 


# Battery Storage
# Domestic Batteries - 2nd life EVs
nUsers1 = 0.028*1985                                                           # domestic storage = domestic PV installations
capacity1 = 40*(1-0.2723)
power1 = 50                                                               
eff1 = 0.8
battery_site1 = AS.PracticalBatteryAsset1(dt, T, capacity1, power1, eff1, nUsers1) 
dispatchable.append(battery_site1)

# Community Battery - Tesla Powerpack
nPacks = 1 
capacity2 = 4200 #6300
power2 = 500
eff2 = 1
battery_site2 = AS.PracticalBatteryAsset2(dt, T, capacity2, power2, eff2, nPacks) 
dispatchable.append(battery_site2)

# V2G Storage - how do we know WHEN (times of day) we can use V2G storage?
nUsers3 = 1                                                                    # EVs in Kennington
capacity3 = 40
power3 = 50
eff3 = 1
battery_site3 = AS.PracticalBatteryAsset3(dt, T, capacity3, power3, eff3, nUsers3) 
dispatchable.append(battery_site3)


# Carbon Emissions Intensities
loss = 0.08                                                                                 # 8% loss from electricity generation to consumption
emission_intensity = EM.Emissions(loss)                                                     # numpy array gCO2/kWh
emission_intensity = [i[0] for i in emission_intensity.getEmissionIntensity().tolist()]     # list gCO2/kWh
emission_intensity = [i/1000000 for i in emission_intensity]                                # list tnCO2/kWh
emission_intensity_means = AV.Averaging(emission_intensity)


############################################
### STEP 3: setup and run the energy system
############################################


all_assets = non_dispatchable + dispatchable

# setup
energy_system = ES.EnergySystem(non_dispatchable, dispatchable, dt, T)

# run
net_load, disp_load, non_disp_load = energy_system.basic_energy_balance()


#######################################
### STEP 4: prepare lists for plotting
#######################################


# _means are lists of 5 nested lists, where each nested list is the average daily profile of over 1/5th of the year
net_load = [i[0] for i in net_load.tolist()]                        # average net load
net_load_means = AV.Averaging(net_load)

disp_load = [i[0] for i in disp_load.tolist()]                      # average net dispatchable load
disp_load_means = AV.Averaging(disp_load)                   

non_disp_load = [i[0] for i in non_disp_load.tolist()]              # average net non-dispatchable load
non_disp_load_means = AV.Averaging(non_disp_load)

pv = [i[0] for i in pv_site1.getOutput(dt).tolist()]                # average domestic pv generation 
pv_means = AV.Averaging(pv)

sf = [i[0] for i in pv_site2.getOutput(dt).tolist()]                # average solar farm generation 
sf_means = AV.Averaging(sf)

hydro = [i[0] for i in hydro_site1.getOutput(dt).tolist()]          # average hydro generation
hydro_means = AV.Averaging(hydro)

dom = [i[0] for i in load_site1.getOutput(dt).tolist()]             # average domestic demand
dom_means = AV.Averaging(dom)

nondom = [i[0] for i in load_site2.getOutput(dt).tolist()]          # average non-domestic demand
nondom_means = AV.Averaging(nondom)

sch = [i[0] for i in load_site7.getOutput(dt).tolist()]             # average schools electricty demand
sch_means = AV.Averaging(sch)

evd = [i[0] for i in load_site3.getOutput(dt).tolist()]             # average EV electricity demand (day)
evd_means = AV.Averaging(evd)

evn = [i[0] for i in load_site9.getOutput(dt).tolist()]             # average EV electricity demand (night)
evn_means = AV.Averaging(evn)

ev = [i+j for i,j in zip(evd,evn)]                                  # average total EV electricity demand
ev_means = AV.Averaging(ev)

hp1 = [i[0] for i in load_site4.getOutput().tolist()]               # average central heat pump electricity demand
hp1_means = AV.Averaging(hp1)

hp2 = [i[0] for i in load_site5.getOutput().tolist()]               # average domestic heat pump electricity demand
hp2_means = AV.Averaging(hp2)

hp3 = [i[0] for i in load_site6.getOutput().tolist()]               # average non-domestic heat pump electricity demand
hp3_means = AV.Averaging(hp3)

hp = [i+j+k for i,j,k in zip(hp1,hp2,hp3)]                          # average total heat pump electricity demand
hp_means = AV.Averaging(hp)

dombat = [i[0] for i in battery_site1.getOutput(net_load).tolist()] # average domestic battery storage
dombat_means = AV.Averaging(dombat)

combat = [i[0] for i in battery_site2.getOutput(net_load).tolist()] # average community battery storage
combat_means = AV.Averaging(combat)

v2g = [i[0] for i in battery_site3.getOutput(net_load).tolist()]    # average V2G battery storage
v2g_means = AV.Averaging(v2g)

gross_gen = [i+j+k for i,j,k in zip(hydro,pv,sf)]                   # average gross renewable generation 
gross_gen_means = AV.Averaging(gross_gen)

gross_load = [i+j+k+l+m for i,j,k,l,m in zip(dom,nondom,sch,ev,hp)]  # average gross demand            # average gross demand without energy system
gross_load_means = AV.Averaging(gross_load)

current = [h+i+j-k for h,i,j,k in zip(sch,dom,nondom,hydro)]        # average net load without energy system (no EV demand included)
current_means = AV.Averaging(current)


#######################################
### STEP 5: plot generation results
#######################################


# overall plotting style
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
### STEP 6: plot load results
#######################################


# 1st 5th of the year     # this is plotting average profiles found over the dates 1st Jan-14th March; the "Average.py" function finds these average profiles over this period
Fig1 = PT.loadPlotting(net_load_means[0], gross_load_means[0], dom_means[0], nondom_means[0], ev_means[0], hp_means[0])
Fig1.canvas.set_window_title('1st Jan - 14th Mar')

# 2nd 5th of the year
Fig2 = PT.loadPlotting(net_load_means[1], gross_load_means[1], dom_means[1], nondom_means[1], ev_means[1], hp_means[1])
Fig2.canvas.set_window_title('15th Mar - 26th May')

# 3rd 5th of the year
Fig3 = PT.loadPlotting(net_load_means[2], gross_load_means[2], dom_means[2], nondom_means[2], ev_means[2], hp_means[2])
Fig3.canvas.set_window_title('27th May - 7th Aug')

# 4th 5th of the year
Fig4 = PT.loadPlotting(net_load_means[3], gross_load_means[3], dom_means[3], nondom_means[3], ev_means[3], hp_means[3])
Fig4.canvas.set_window_title('8th Aug - 19th Oct')

# 5th 5th of the year
Fig5 = PT.loadPlotting(net_load_means[4], gross_load_means[4], dom_means[4], nondom_means[4], ev_means[4], hp_means[4])
Fig5.canvas.set_window_title('20th Oct - 31st Dec') 


##########################################
### STEP 7: calculate and plot emissions
##########################################


# calculate CO2 emissions with/without the energy system
x0 = emission_intensity                                     # carbon emission intensities (tnCO2/kWh) 
y0 = net_load                                               # with energy system, net load (kWh)
z0 = current                                                # without energy system, net load (kWh)  
                                 
emissions = [a*b for a,b in zip(y0,x0)]                     # with energy system, emissions (tnCO2)
emissions_means = AV.Averaging(emissions)                   # daily averages for each quintile
                                     
previous_emissions = [a*b for a,b in zip(z0,x0)]            # without energy system, emissions (tnCO2)
previous_emissions_means = AV.Averaging(previous_emissions) # daily averages for each quintile


# plot emmissions intensity over 2020
figA,axA = plt.subplots()
figA.tight_layout(pad=3.0)
x_axis = pd.date_range('2020' + '-01-01', periods = 17520, freq= '0.5H') 
myFmt = mdates.DateFormatter('%H:%M')                       # format the times into Hour:Minute format
plt.gcf().autofmt_xdate()                                   # automatic rotation of the axis plots

axA.plot(x_axis, emission_intensity)
axA.set_ylabel('tnCO2/kWh')
axA.set_xlabel('Time')
axA.set_title('Emissions Intensity, 2020')
axA.xaxis.set_major_formatter(myFmt)                        # apply HH:MM format to the x axis data
figA.canvas.set_window_title('1st Jan - 31st Dec')


# plot net load over 2020
figB,axB = plt.subplots()
figB.tight_layout(pad=3.0)
x_axis = pd.date_range('2020' + '-01-01', periods = 17520, freq= '0.5H') 
myFmt = mdates.DateFormatter('%H:%M')                       # format the times into Hour:Minute format
plt.gcf().autofmt_xdate()                                   # automatic rotation of the axis plots

axB.plot(x_axis, net_load)
axB.set_ylabel('kWh')
axB.set_xlabel('Time')
axB.set_title('Net Load, 2020')
axB.xaxis.set_major_formatter(myFmt)                        # apply HH:MM format to the x axis data
figB.canvas.set_window_title('1st Jan - 31st Dec')


# plot CO2 emissions over 2020 
figC,axC = plt.subplots()
figC.tight_layout(pad=3.0)
x_axis = pd.date_range('2020' + '-01-01', periods = 17520, freq= '0.5H') 
myFmt = mdates.DateFormatter('%H:%M')                       # format the times into Hour:Minute format
plt.gcf().autofmt_xdate()                                   # automatic rotation of the axis plots

axC.plot(x_axis, emissions)
axC.set_ylabel('tnCO2')
axC.set_xlabel('Time')
axC.set_title('Net CO2 Emissions, 2020')
axC.xaxis.set_major_formatter(myFmt)                        # apply HH:MM format to the x axis data
figC.canvas.set_window_title('1st Jan - 31st Dec')


# plot average daily emissions for each quintile in 2020
figD = PT.emPlotting(emissions_means[0], emissions_means[1], emissions_means[2], emissions_means[3],  emissions_means[4])
figD.canvas.set_window_title('Average Daily Emissions In Each Quintile')


# find annualised net load and total emissions with the energy system
print("")
print("2020 Load & Emissions Figures")
print("")
#print("New Energy System, Annual Net Emissions: %.2f tnCO2" % (sum(emissions)))
#print("")
print("New Energy System, Annual Net Load: %.2f MWh" % (sum(net_load)/1000))
print("")


# find annualised net load and total emissions without the energy system
#print("Current Situation, Annual Net Emissions: %.2f tnCO2" % sum(previous_emissions))
#print("")
print("Current Situation, Annual Net Load: %.2f MWh" % (sum(current)/1000))
print("")
#print("Annual Net Emissions Saving With New Energy System: %.2f tnCO2" % (sum(previous_emissions)-sum(emissions)))
#print("")


#######################################
### STEP 8: setup and run the market
#######################################


# setup
grid_sale_price = 0.055                                                          # price paid for exports (£/kWh) grid/Octopus
market1 = MK.marketObject(energy_system, export_rate= grid_sale_price) 

# run
opCost = market1.getTotalCost()
grid_cost = market1.getGridCost().sum()
print("Annual Network Cost: £ %.2f" % (grid_cost / 100))
purchased, sold = market1.gridBreakdown()

# convert to pounds
purchased_daily = ES.E_to_dailyE(purchased, dt) / 100 
sold_daily = ES.E_to_dailyE(sold, dt) / 100           


#plt.show()