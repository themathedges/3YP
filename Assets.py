#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3YP basic asset module.
Adapted from UoO EPG's energy management framework.
Authors: Avinash Vijay, Scot Wheeler
"""

__version__ = '0.4'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta


class Non_Dispatchable:
    """Non-dispatchable asset base class"""
    def __init__(self):
        self.dispatch_type = "Non-dispatchable"
        self.capacity = 0
        self.install_cost = 0
        self.lifetime = 25
        self.genFiT = 5.24 # feed in tariff p/kWh


class Dispatchable:
    """Dispatchable asset base class"""
    def __init__(self):
        self.dispatch_type = "Dispatchable"
        self.capacity = 0
        self.install_cost = 0
        self.lifetime = 25
        self.genFiT = 5.24 # feed in tariff p/kWh


class pvAsset(Non_Dispatchable):
    """
    PV asset class

    Parameters
    ----------
    profile_filepath : str
            Filepath for the profile
    
    Capacity : float
        PV capacity, kW.

    install_cost : float
        £ price per kWp to install
        
    maintenance_cost : float
        Annual maintenance cost in £s
    """
    def __init__(self, pvCapacity, pvInstallations, profile_filepath='data/oxon_solar_2014.csv', install_cost=(6000/4),
                 maintenance=100, **kwargs):
        super().__init__()
        self.profile_filepath = profile_filepath
        self.pvCapacity = pvCapacity
        self.asset_type = 'PV'
        self.install_cost = install_cost * 100  # p/kWp
        self.maintenance = maintenance * 100 # p per year
        self.cf = self.solarProfile()
        self.pvInstallations = pvInstallations
        
    def solarProfile(self):
        """
        Loads the kW/kWp hourly solar profile


        Returns
        -------
        kW/kWp solar profile

        """
        df = pd.read_csv(self.profile_filepath, index_col=0,
                         parse_dates=True, dayfirst=True)  # kW/kWp
        print('original solar data coming...')
        print(df.info())
        print(df.head(50))
        return df  

    def getOutput(self, dt):
        """
        Return PV output

        Parameters
        ----------
        dt : float
            Time interval (hours)

        Returns
        -------
        PV output : numpy array
        """
        cfHH = self.cf.resample('0.5H').mean()
        # adding a missing point at the end
        cfHH = cfHH.append(pd.DataFrame({cfHH.columns[0]: np.nan},
                                      index=[(cfHH.index[-1] +
                                              timedelta(minutes=30))]))
        cfHH = cfHH.interpolate()
        print('modified solar data coming...')
        print(cfHH.info())
        print(cfHH.head(50))
        output = cfHH.values * self.pvCapacity * self.pvInstallations * dt # kWh
        self.output = output
        print('solar output coming...')
        print(output)
        return output


class loadAsset(Non_Dispatchable):
    """
    Load asset class

    Parameters
    ----------
    nHouses : int
        Number of houses
        
    profile_filepath : str
        Filepath to load profile
    """
    def __init__(self, nHouseholds=1728, profile_filepath='data/ken_dom_annual_demand_per_user.csv', **kwargs):
        super().__init__()
        self.nHouseholds = nHouseholds
        self.asset_type = 'DOMESTIC_LOAD'
        self.install_cost = 0
        self.profile_filepath = profile_filepath
        self.profile = self.loadProfile()
        
    def loadProfile(self):
        df = pd.read_csv(self.profile_filepath, usecols=[1]) # kW
        print('domestic load data coming...')
        print(df.info())
        print(df.head(50))
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
        dem = self.profile.values   # this will return the 365*48 values in the load profile at a numpy array 
        output = dem * self.nHouses * dt # kWh 
        self.output = output
        print('domestic load output coming...')
        print(output)
        return output


class ndAsset(Non_Dispatchable):
    #"""
    #Load asset class

    #Parameters
    #----------
    #nInstallations : int
        #Number of installations
        
    #profile_filepath : str
        #Filepath to load profile
    
    def __init__(self, nInstallations=36, profile_filepath='data/ken_non_dom_annual_demand_per_user.csv', **kwargs):
        super().__init__()
        self.nInstallations = nInstallations
        self.asset_type = 'NON_DOMESTIC_LOAD'
        self.install_cost = 0
        self.profile_filepath = profile_filepath
        self.profile = self.ndProfile()
        
    def ndProfile(self):
        df = pd.read_csv(self.profile_filepath, usecols=[1]) # kW
        print('non-domestic load data coming...')
        print(df.info())
        print(df.head(50))
        return df
        
    def getOutput(self, dt):
       
        #Return non-domestic demand

        #Parameters
        #----------
        #dt : float
           # Time interval (hours)

        #Returns
        #-------
        #Non-domestic demand : numpy array
        
        dem = self.profile.values
        output = dem * self.nInstallations * dt # kWh
        self.output = output
        print('non-domestic load output coming...')
        print(output)
        return output
    


#class hpAsset(Dispatchable):

    #Heat Pump asset class

    #Parameters
    #----------
    #nHouses : int
    #    Number of houses
        
    #profile_filepath : str
    #    Filepath to load profile

    """
    def __init__(self, nHouses=1700, profile_filepath='?', **kwargs):
        super().__init__()
        self.nHouses = nHouses
        self.asset_type = 'HEAT_PUMP_LOAD'
        self.install_cost = 0
        self.profile_filepath = profile_filepath
        self.profile = self.hpProfile()
        
    def hpProfile(self):
        df = pd.read_csv(self.profile_filepath, usecols=[1]) # kW
        print('heat pump load data coming...')
        print(df.info())
        print(df.head(50))
        return df
        
    def getOutput(self, dt):
    
        #Return heat pump electricity demand

        #Parameters
        #----------
        #dt : float
        #    Time interval (hours)

        #Returns
        #-------
        #Heat pump electricity demand : numpy array
        
        hp = self.profile.values
        output = hp * self.nHouses * dt # kWh
        self.output = output
        print('heat pump load output coming...')
        print(output)
        return output
    """

class PracticalBatteryAsset1(Dispatchable):
    """
    1st life EV battery asset class

    Parameters
    ----------
    capacity : float
        Battery capacity, kWh.

    power : float
        Maximum power, kW.

    eff : float
        Charging/discharging efficiency between 0-1.

    dt : float
        Time interval (hours)

    T : int
        Number of intervales
        
    install_cost : float
        Install cost in £/kWh
    """
    def __init__(self, dt, T, capacity, power, eff, nUsers1, install_cost=(27000/36)):
        super().__init__()
        self.nUsers1 = nUsers1
        self.asset_type = '1_LIFE_EV_BATTERY'
        self.capacity = capacity * self.nUsers1
        self.power = power * dt
        self.eff = eff
        self.soc = np.ones(T) * self.capacity
        self.install_cost = install_cost * 100  # p/kWh

    def getOutput(self, net_load):
        """
        Battery control of charging/discharging in response to net load.

        Parameters
        ----------
        net_load : numpy array
            The net load, (load - nondispatchable gen).

        Returns
        -------
        Battery energy use profile : numpy array
        """
        T = len(net_load)
        output = np.zeros((T, 1))
        for j in range(len(net_load)):
            if j == 0:
                soc = self.capacity
            else:
                soc = self.soc[j-1]

            if net_load[j] > 0:  # use battery
                output[j] = min(self.power, net_load[j], self.eff*soc)
                self.soc[j] = soc - (1/self.eff)*output[j]
            elif net_load[j] < 0:  # charge battery
                output[j] = max(-self.power, net_load[j],
                                - (1/self.eff) * (self.capacity - soc))
                self.soc[j] = soc - self.eff * output[j]
            elif net_load[j] == 0:  # do nothing
                self.soc[j] = soc
        self.output = output
        return output


class PracticalBatteryAsset2(Dispatchable):
    """
    Practical battery asset class

    Parameters
    ----------
    capacity : float
        Battery capacity, kWh.

    power : float
        Maximum power, kW.

    eff : float
        Charging/discharging efficiency between 0-1.

    dt : float
        Time interval (hours)

    T : int
        Number of intervales
        
    install_cost : float
        Install cost in £/kWh
    """
    def __init__(self, dt, T, capacity, power, eff, nUsers2, install_cost=500):
        super().__init__()
        self.nUsers2 = nUsers2
        self.asset_type = '2_LIFE_EV_BATTERY'
        self.capacity = 0.8 * capacity * self.nUsers2
        self.power = power * dt
        self.eff = eff
        self.soc = np.ones(T) * self.capacity
        self.install_cost = install_cost * 100  # p/kWh

    def getOutput(self, net_load):
        """
        Battery control of charging/discharging in response to net load.

        Parameters
        ----------
        net_load : numpy array
            The net load, (load - nondispatchable gen).

        Returns
        -------
        Battery energy use profile : numpy array
        """
        T = len(net_load)
        output = np.zeros((T, 1))
        for j in range(len(net_load)):
            if j == 0:
                soc = self.capacity
            else:
                soc = self.soc[j-1]

            if net_load[j] > 0:  # use battery
                output[j] = min(self.power, net_load[j], self.eff*soc)
                self.soc[j] = soc - (1/self.eff)*output[j]
            elif net_load[j] < 0:  # charge battery
                output[j] = max(-self.power, net_load[j],
                                - (1/self.eff) * (self.capacity - soc))
                self.soc[j] = soc - self.eff * output[j]
            elif net_load[j] == 0:  # do nothing
                self.soc[j] = soc
        self.output = output
        return output


class hydroAsset(Non_Dispatchable):
    """
    Sandford hydro asset class

    Parameters

    ----------
    capacity : float
        Maximum power, kW.

    dt : float
        Time interval (hours)

    T : int
        Number of intervales
        
    maintenance_cost : float
        Annual maintenance cost in £s
    """
    def __init__(self, hydroCapacity, profile_filepath='data/Sandford_hydro_generation_30_min_date.csv', maintenance=100000, **kwargs):
        super().__init__()
        self.hydroCapacity = hydroCapacity
        self.asset_type = 'HYDRO'
        self.maintenance = maintenance * 100 # p per year
        self.genFiT = 5.24  # p/kWh     
        self.profile_filepath = profile_filepath
        self.profile = self.hydroProfile()
        
    def hydroProfile(self):
        df = pd.read_csv(self.profile_filepath, usecols=[1], 
                         parse_dates=True, dayfirst=True) # kW
        print('hydro data coming...')
        print(df.info())
        print(df.head(50))
        return df 

    def getOutput(self, dt):
        """
        Return Sandford Hydro output

        Parameters
        ----------
        dt : float
            Time interval (hours)

        Returns
        -------
        Sandford Hydro output : numpy array
        """
        gen = self.profile.values
        output = gen * dt # kWh
        self.output = output
        print('hydro output coming...')
        print(output)
        return output

if __name__ == "__main__":
    pass

