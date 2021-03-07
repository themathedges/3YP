#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic emissions calculator file.
Author: Mathew Hedges
"""

__version__ = '0.1'

# import modules
import pandas as pd
import numpy as np
from datetime import timedelta


class Emissions():
    """
    Emissions calculator class

    Parameters
    ----------
    Loss : int
        % Losses between generation and consumption of grid power
        
    profile_filepath : str
        Filepath to load profile
    """
    def __init__(self, nHouseholds, profile_filepath='data/ken_dom_annual_demand_per_household.csv', **kwargs):    
        super().__init__()
        self.nHouseholds = nHouseholds
        self.asset_type = 'DOMESTIC_LOAD'
        self.install_cost = 0
        self.profile_filepath = profile_filepath
        self.profile = self.loadProfile()
        
    def loadProfile(self):
        df = pd.read_csv(self.profile_filepath, usecols=[1]) # kW
        #print('domestic load data coming...')
        #print(df.info())
        #print(df.head(50))
        return df
        
    def getOutput(self, dt):
        """
        Return domestic demand

        Parameters
        ----------
        dt : float
            Time interval (hours)

        Returns
        -------
        Domestic demand : numpy array
        """
        dem = self.profile.values   # this will return the 365*48 values in the dom load profile as a numpy array 
        output = dem * self.nHouseholds * dt # kWh 
        self.output = output
        #print('domestic load output coming...')
        #print(output)
        return output