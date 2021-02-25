#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
basic averaging and plotting file.
Author: Mathew Hedges
"""

__version__ = '0.1'

# import modules
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import datetime
from pandas import Timestamp

def Averaging():
    #y0 = asset_list
    print('hello bitch')
    y0 = hydro_list1
    print(type(y0))
    print(len(y0))
    print('goodbye bitch')

    y1 = y0[0:3504] # 1/5th of a years worth of halfhours
    y2 = y0[3504:7008]
    y3 = y0[7008:10512]
    y4 = y0[10512:14016]
    y5 = y0[14016:17519]

    x1 = np.zeros((73,48)) # 1/5th of a years worth of days
    x2 = np.zeros((73,48))
    x3 = np.zeros((73,48))
    x4 = np.zeros((73,48))
    x5 = np.zeros((72,48)) # skipping the last day in the last 1/5th because it only has 47 halfhours which is messing up the average!


    for i in range(73): 
        x1[i] = y1[i*48:(i+1)*48] # put each day's half hours into the rows of x
    print('mean y1...')
    print(np.mean(x1, axis=0)) # find the mean of the halfhours over every day


    for i in range(73):
        x2[i] = y2[i*48:(i+1)*48] # put each day's half hours into the rows of x
    print('mean y2...')
    print(np.mean(x2, axis=0)) # find the mean of the halfhours over every day


    for i in range(73):
        x3[i] = y3[i*48:(i+1)*48] # put each day's half hours into the rows of x
    print('mean y3...')
    print(np.mean(x3, axis=0)) # find the mean of the halfhours over every day


    for i in range(73):
        x4[i] = y4[i*48:(i+1)*48] # put each day's half hours into the rows of x
    print('mean y4...')
    print(np.mean(x4, axis=0)) # find the mean of the halfhours over every day


    for i in range(72):
        x5[i] = y5[i*48:(i+1)*48] # put each day's half hours into the rows of x
    print('mean y5...')
    print(np.mean(x5, axis=0)) # find the mean of the halfhours over every day
