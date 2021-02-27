#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic averaging file.
The output of each asset y, in halfhours over the whole year,
is split into 5 consecutive blocks. These are entered into numpy
arrays x in which the rows represent consecutive days in that
block and the columns represent all the halfhours in that day.
The average day in that block is then found and returned as a list of numpy arrays.
Author: Mathew Hedges
"""

__version__ = '0.1'

# import modules
import numpy as np


def Averaging(asset_list):
    # import the relevant list of 1 year's worth of halfhours (17520)
    y0 = asset_list 


    # split the list into 5 1/5ths of a year's worth of halfhours (3504)
    y1 = y0[0:3504]
    y2 = y0[3504:7008]
    y3 = y0[7008:10512]
    y4 = y0[10512:14016]
    y5 = y0[14016:17519]


    # prepare numpy arrays to fill with each of the days in 1/5th of a year (73)
    x1 = np.zeros((73,48))
    x2 = np.zeros((73,48))
    x3 = np.zeros((73,48))
    x4 = np.zeros((73,48))
    x5 = np.zeros((72,48)) # skipping the last day in the last 1/5th because it only has 47 halfhours which is messing up the averaging!


    # find the means of the 48 halfhours over the 73 days in each 1/5th of the year
    for i in range(73): 
        x1[i] = y1[i*48:(i+1)*48] # put each day's half hours into the rows of x
    
    mean1 = np.mean(x1, axis=0)   # find the mean of the halfhours over every day


    for i in range(73):
        x2[i] = y2[i*48:(i+1)*48] # put each day's half hours into the rows of x
  
    mean2 = np.mean(x2, axis=0)   # find the mean of the halfhours over every day


    for i in range(73):
        x3[i] = y3[i*48:(i+1)*48] # put each day's half hours into the rows of x
    
    mean3 = np.mean(x3, axis=0)   # find the mean of the halfhours over every day


    for i in range(73):
        x4[i] = y4[i*48:(i+1)*48] # put each day's half hours into the rows of x
    
    mean4 = np.mean(x4, axis=0)   # find the mean of the halfhours over every day


    for i in range(72):
        x5[i] = y5[i*48:(i+1)*48] # put each day's half hours into the rows of x
    
    mean5 = np.mean(x5, axis=0)   # find the mean of the halfhours over every day


    # return a list of 5 means
    return [mean1, mean2, mean3, mean4, mean5] 


if __name__ == "__main__":
    pass