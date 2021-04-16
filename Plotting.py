#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic plotting file.
The mean day for each asset class from a 
given 1/5th of the year is plotted here.
Author: Mathew Hedges
"""

__version__ = '0.2'

# import modules
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import datetime
from pandas import Timestamp    
    
    
def loadPlotting(net_load_mean, non_disp_load_mean, dom_mean, nondom_mean, ev_mean, hp_mean):

    fig,ax =  plt.subplots(nrows=3,ncols=2,sharex=True,sharey=False)
    plt.xticks(rotation=90)
    fig.tight_layout(pad=3.0)
    
    x_axis = pd.date_range('2020' + '-01-01', periods = 48, freq= '0.5H') 
    myFmt = mdates.DateFormatter('%H:%M')       # format the times into Hour:Minute format
    plt.gcf().autofmt_xdate()                   # automatic rotation of the axis plots

    ax[0][0].plot(x_axis, net_load_mean, 'k')
    ax[0][0].set_ylabel('kWh')
    ax[0][0].set_xlabel('Time')
    ax[0][0].set_title('Net Load')
    ax[0][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[0][0].grid(b=True)

    ax[0][1].plot(x_axis, non_disp_load_mean, 'k')
    ax[0][1].set_ylabel('kWh')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_title('Current Gross Non-dispatchable Load') # dom + nondom - hydro
    ax[0][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[0][1].grid(b=True)

    ax[1][0].plot(x_axis, dom_mean, 'k')
    ax[1][0].set_ylabel('kWh')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_title('Domestic Load')
    ax[1][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[1][0].grid(b=True)

    ax[1][1].plot(x_axis, nondom_mean, 'k')
    ax[1][1].set_ylabel('kWh')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_title('Non-domestic Load')
    ax[1][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[1][1].grid(b=True)
    
    ax[2][0].plot(x_axis, ev_mean, 'k')
    ax[2][0].set_ylabel('kWh')
    ax[2][0].set_xlabel('Time')
    ax[2][0].set_title('Electric Vehicle Load')
    ax[2][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data

    ax[2][1].plot(x_axis, hp_mean, 'k')
    ax[2][1].set_ylabel('kWh')
    ax[2][1].set_xlabel('Time')
    ax[2][1].set_title('Heat Pump Load')
    ax[2][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[2][1].grid(b=True)
    
    return fig


def genPlotting(hydro_mean, pv_mean, sf_mean, net_load_mean, gross_gen_mean, disp_load_mean):

    fig,ax =  plt.subplots(nrows=3,ncols=2,sharex=True,sharey=False)
    plt.xticks(rotation=90)
    fig.tight_layout(pad=3.0)
    
    x_axis = pd.date_range('2020' + '-01-01', periods = 48, freq= '0.5H') 
    myFmt = mdates.DateFormatter('%H:%M')       # format the times into Hour:Minute format
    plt.gcf().autofmt_xdate()                   # automatic rotation of the axis plots

    ax[2][0].plot(x_axis, disp_load_mean, 'k')
    ax[2][0].set_ylabel('kWh')
    ax[2][0].set_xlabel('Time')
    ax[2][0].set_title('Net Dispatchable Load')
    ax[2][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[2][0].grid(b=True)

    ax[1][0].plot(x_axis, gross_gen_mean, 'k')
    ax[1][0].set_ylabel('kWh')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_title('Gross Generation')
    ax[1][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[1][0].grid(b=True)

    ax[0][0].plot(x_axis, net_load_mean, 'k')
    ax[0][0].set_ylabel('kWh')
    ax[0][0].set_xlabel('Time')
    ax[0][0].set_title('Net Load')
    ax[0][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[0][0].grid(b=True)

    ax[0][1].plot(x_axis, hydro_mean, 'k')
    ax[0][1].set_ylabel('kWh')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_title('Hydro Generation')
    ax[0][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[0][1].grid(b=True)

    ax[1][1].plot(x_axis, pv_mean, 'k')
    ax[1][1].set_ylabel('kWh')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_title('PV Generation')
    ax[1][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[1][1].grid(b=True)
 
    ax[2][1].plot(x_axis, sf_mean, 'k')
    ax[2][1].set_ylabel('kWh')
    ax[2][1].set_xlabel('Time')
    ax[2][1].set_title('Solar Farm Generation')
    ax[2][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[2][1].grid(b=True)
    
    return fig


def emPlotting(emissions1, emissions2, emissions3, emissions4, emissions5, emissions6):

    fig,ax =  plt.subplots(nrows=3,ncols=2,sharey=False, sharex=False)
    plt.xticks(rotation=90)
    fig.tight_layout(pad=3.0)
    
    x_axis = pd.date_range('2020' + '-01-01', periods = 48, freq= '0.5H')
    myFmt = mdates.DateFormatter('%H:%M')       # format the times into Hour:Minute format
    plt.gcf().autofmt_xdate()                   # automatic rotation of the axis plots

    ax[0][0].plot(x_axis, emissions1, 'k')
    ax[0][0].set_ylabel('tnCO2')
    ax[0][0].set_xlabel('Time')
    ax[0][0].set_title('Net Emissions, 1st Quintile Daily Average')
    ax[0][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[0][0].grid(b=True)

    ax[1][0].plot(x_axis, emissions2, 'k')
    ax[1][0].set_ylabel('tnCO2')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_title('Net Emissions, 2nd Quintile Daily Average')
    ax[1][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[1][0].grid(b=True)

    ax[2][0].plot(x_axis, emissions3, 'k')
    ax[2][0].set_ylabel('tnCO2')
    ax[2][0].set_xlabel('Time')
    ax[2][0].set_title('Net Emissions, 3rd Quintile Daily Average')
    ax[2][0].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[2][0].grid(b=True)

    ax[0][1].plot(x_axis, emissions4, 'k')
    ax[0][1].set_ylabel('tnCO2')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_title('Net Emissions, 4th Quintile Daily Average')
    ax[0][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[0][1].grid(b=True)

    ax[1][1].plot(x_axis, emissions5, 'k')
    ax[1][1].set_ylabel('tnCO2')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_title('Net Emissions, 5th Quintile Daily Average')
    ax[1][1].xaxis.set_major_formatter(myFmt)   # apply HH:MM format to the x axis data
    ax[1][1].grid(b=True)

    x_axis2 = pd.date_range('2020' + '-01-01', periods = 17520, freq= '0.5H')    # different x-axis for annual data 
    myFmt2 = mdates.DateFormatter('%B')                                          # format the times into month format

    ax[2][1].plot(x_axis2, emissions6, 'k')
    ax[2][1].set_ylabel('tnCO2')
    #ax[2][1].set_xlabel('Time')
    ax[2][1].set_title('Net Emissions, Annual')
    ax[2][1].xaxis.set_major_formatter(myFmt2)   # apply HH:MM format to the x axis data
    ax[2][1].grid(b=True)
    
    return fig


if __name__ == "__main__":
    pass