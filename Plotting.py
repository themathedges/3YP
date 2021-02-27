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
    
    
def Plotting(net_load_mean, disp_load_mean, non_disp_load_mean, pv_mean, hydro_mean, dom_mean, nondom_mean, dombat_mean, combat_mean): #, ev_mean, hp_mean, sf_mean):

    fig,ax =  plt.subplots(nrows=6,ncols=2,sharex=True,sharey=False)
    plt.xticks(rotation=90)
    fig.tight_layout(pad=3.0)
    
    x_axis = pd.date_range('2018' + '-01-01', periods = 48, freq= '0.5H') 
    myFmt = mdates.DateFormatter('%H:%M')       # format the times into Hour:Minute format
    plt.gcf().autofmt_xdate()                   # automatic rotation of the axis plots

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

    ax[3][0].plot(x_axis, nondom_mean)
    ax[3][0].set_ylabel('kWh')
    ax[3][0].set_xlabel('Time')
    ax[3][0].set_title('Non-domestic Load')
    ax[3][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[3][1].plot(x_axis, hydro_mean)
    ax[3][1].set_ylabel('kWh')
    ax[3][1].set_xlabel('Time')
    ax[3][1].set_title('Hydro Generation')
    ax[3][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    #ax[4][0].plot(x_axis, hp_mean)
    ax[4][0].set_ylabel('kWh')
    ax[4][0].set_xlabel('Time')
    ax[4][0].set_title('Heat Pump Load')
    ax[4][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[4][1].plot(x_axis, pv_mean)
    ax[4][1].set_ylabel('kWh')
    ax[4][1].set_xlabel('Time')
    ax[4][1].set_title('PV Generation')
    ax[4][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    #ax[5][0].plot(x_axis, ev_mean)
    ax[5][0].set_ylabel('kWh')
    ax[5][0].set_xlabel('Time')
    ax[5][0].set_title('Electric Vehicle Load')
    ax[5][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    #ax[5][1].plot(x_axis, sf_mean)
    ax[5][1].set_ylabel('kWh')
    ax[5][1].set_xlabel('Time')
    ax[5][1].set_title('Solar Farm Generation')
    ax[5][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    return fig


if __name__ == "__main__":
    pass