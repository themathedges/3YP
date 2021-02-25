#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic plotting file.
The mean day for each asset class from a 
given 1/5th of the year is plotted here.
Author: Mathew Hedges
"""

__version__ = '0.1'

# import modules
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import datetime
from pandas import Timestamp    
    
    
def Plotting(net_load_mean, disp_load_mean, non_disp_load_mean, pv_mean, hydro_mean, dom_mean, dombat_mean, combat_mean):

    fig,ax =  plt.subplots(nrows=4,ncols=2,sharex=True,sharey=False)
    plt.xticks(rotation=90)
    fig.tight_layout(pad=3.0)
    #x_axis = pd.date_range(datetime.time(hour=0, minute=0, second=0), datetime.time(hour=23, minute=59, second=59), freq='0.5H')
    #x_axis = pd.timedelta_range(start='1 day', periods=48, freq='0.5H')
    #x_axis = [datetime.time(0, 0, 0, 0) + timedelta(hours=0.5*i) for i in range(24)]

    x_axis = pd.date_range('2018' + '-01-01', periods = 48, freq= '0.5H') 
    myFmt = mdates.DateFormatter('%H:%M')   # format the times into Hour:Minute format
    plt.gcf().autofmt_xdate()               # automatic rotation of the axis plots

    ax[0][0].plot(x_axis, net_load_mean)
    ax[0][0].set_ylabel('kWh')
    ax[0][0].set_xlabel('Time')
    ax[0][0].set_title('Net Load')
    ax[0][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[0][1].plot(x_axis, non_disp_load_mean)
    ax[0][1].set_ylabel('kWh')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_title('Net Non-dispatchable Load')
    ax[0][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[1][0].plot(x_axis, disp_load_mean)
    ax[1][0].set_ylabel('kWh')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_title('Net Dispatchable Load')
    ax[1][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[1][1].plot(x_axis, dombat_mean)
    ax[1][1].set_ylabel('kWh')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_title('Domestic Battery SOC')
    ax[1][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[2][0].plot(x_axis, dom_mean)
    ax[2][0].set_ylabel('kWh')
    ax[2][0].set_xlabel('Time')
    ax[2][0].set_title('Domestic Load')
    ax[2][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[2][1].plot(x_axis, combat_mean)
    ax[2][1].set_ylabel('kWh')
    ax[2][1].set_xlabel('Time')
    ax[2][1].set_title('Community Battery SOC')
    ax[2][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[3][0].plot(x_axis, pv_mean)
    ax[3][0].set_ylabel('kWh')
    ax[3][0].set_xlabel('Time')
    ax[3][0].set_title('PV Generation')
    ax[3][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[3][1].plot(x_axis, hydro_mean)
    ax[3][1].set_ylabel('kWh')
    ax[3][1].set_xlabel('Time')
    ax[3][1].set_title('Hydro Generation')
    ax[3][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    return fig


# ignore
#print('mine')
#print(pd.date_range(start=datetime.datetime(year=2018,month=1,day=1,hour=0,minute=0), periods=48, freq='0.5H'))
#print('theirs')
#print(pd.date_range(datetime.datetime(2017,1,1), datetime.datetime(2017, 12, 31, 23, 59, 59), freq='0.5H'))

if __name__ == "__main__":
    pass
