#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic emissions calculator file.
Caron emissions intensity data (generation) for
the year 2020 is imported as a CSV file into a 
pandas dataframe and then converted to a numpy 
array for outputting. Losses between generation 
and consumption are included using a loss factor.
Author: Mathew Hedges
"""

__version__ = '0.1'

# import modules
import pandas as pd
import numpy as np


class Emissions:
    """
    Emissions calculator class

    Parameters
    ----------
    Loss : int
        % Losses between generation and consumption of grid power
        
    profile_filepath : str
        Filepath to load profile
    """
    def __init__(self, loss, profile_filepath='data/Carbon_Intensity_Data_2020.csv', **kwargs):    
        super().__init__()
        loss_factor = 1 / (1 - loss)
        self.loss_factor = loss_factor
        self.profile_filepath = profile_filepath
        self.profile = self.co2Profile()
        
    def co2Profile(self):
        df = pd.read_csv(self.profile_filepath, usecols=[0]) # gCO2 / kWh
        print('carbon intensity of electricity generation (data) coming...')
        print(df.info())
        print(df.head(50))
        return df
        
    def getEmissionIntensity(self):
        """
        Return carbon intensity of electricity consumption

        Parameters
        ----------
        dt : float
            Time interval (hours)

        Returns
        -------
        Carbon intensity of consumption : numpy array
        """
        gen_intensity = self.profile.values # gCO2 / kWh
        con_intensity = gen_intensity * self.loss_factor # gCO2 / kWh 
        self.con_intensity = con_intensity
        print('carbon intensity of electricity consumption (output) coming...')
        print(con_intensity)
        return con_intensity


if __name__ == "__main__":
    pass