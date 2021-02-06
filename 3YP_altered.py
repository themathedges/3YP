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
#import Market as MK


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

# PV generation
pv_site1 = AS.pvAsset() # using 1500 of these for every house in K
non_dispatchable.append(pv_site1)

# Load
load_site1 = AS.loadAsset() # using 1700 of these for every household in K
non_dispatchable.append(load_site1)

# Battery storage
battery_site1 = AS.PracticalBatteryAsset1(dt, T) # using 700 1st life EVs
dispatchable.append(battery_site1)
battery_site2 = AS.PracticalBatteryAsset2(dt, T) # using 200 2nd life EVs
dispatchable.append(battery_site2)

# Hydro generation
hydro_site1 = AS.hydroAsset()
non_dispatchable.append(hydro_site1)

#######################################
#STEP 4: setup and run the energy system
#######################################

all_assets = non_dispatchable + dispatchable

# setup
energy_system = ES.EnergySystem(non_dispatchable, dispatchable, dt, T)
# run
net_load = energy_system.basic_energy_balance()

#######################################
### STEP 6: setup and run the market
#######################################

# no

# #######################################
# ### STEP 7: plot results
# #######################################

#plt.stackplot(np.array(range(48)), pv_site1.output)#, hydro_site1.output)
x_axis = pd.date_range(datetime.datetime(2017,1,1), datetime.datetime(2017, 12, 31, 23, 59, 59), freq='0.5H')
#labels = ['PV Output']#, 'Hydro Operation']
#ax = plt.subplot(1,1,1)
#p1 = plt.stackplot(x_axis, pv_site1.output.T, battery_site1.output.T, labels=labels)
#plt.plot(x_axis, net_load, '-k', label='Load')
plt.plot(x_axis[1:48], net_load[1:48])
#plt.xticks(range(365*48, (365*48)/12))
#ax.set_xticklabels(['00:00','06:00','12:00','18:00','00:00'])
plt.ylabel('kWh', color='k')
plt.xlabel('Time', color='k')
#ax.legend()
#ax.format_xdata = mdates.DateFormatter('%m')
#ax.autofmt_xdate()
#plt.legend()
#plt.plot(battery_site1.soc/battery_site1.capacity)
plt.show()
#plt.pause(0.01)


# plot data together
#fig,ax =  plt.subplots(nrows=3,ncols=2,sharex=True,sharey=False)
#fig.tight_layout(pad=3.0)
#x_axis = pd.date_range(datetime.datetime(2017,1,1), datetime.datetime(2017, 12, 31, 23, 59, 59), freq='0.5H')
#plt.xticks(range(365*48, round((365*48)/12)), labels = ['00:00','06:00','12:00','18:00','00:00'])
#ax.format_xdata = mdates.DateFormatter('%m')
#ax.autofmt_xdate()

#ax[0][0].plot(x_axis, net_load)
#ax[0][0].set_ylabel('Net Load')
#ax[0][0].set_xlabel('Time')
#ax[0][0].set_title('1')

#ax[0][1].plot(load_site1.output.T)
#ax[0][1].set_ylabel('Demand')
#ax[0][1].set_xlabel('Time')
#ax[0][1].set_title('2')

#ax[1][0].plot(battery_site1.output.T)
#ax[1][0].set_ylabel('1st Life EV')
#ax[1][0].set_xlabel('Time')
#ax[1][0].set_title('3')

#ax[1][1].plot(battery_site2.output.T)
#ax[1][1].set_ylabel('2nd Life EV')
#ax[1][1].set_xlabel('Time')
#ax[1][1].set_title('4')

#ax[0][2].plot(pv_site1.output.T)
#ax[0][2].set_ylabel('PV')
#ax[0][2].set_xlabel('Time')
#ax[0][2].set_title('4')

#ax[1][2].plot(all_assets)
#ax[1][2].set_ylabel('Net Load aswell?')
#ax[1][2].set_xlabel('Time')
#ax[1][2].set_title('4')

#plt.show()