#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3YP basic Energy System module.
Adapted from UoO EPG's energy management framework.
Authors: Avinash Vijay, Scot Wheeler, Mathew Hedges
"""

__version__ = '0.4'

# import modules
import numpy as np


class EnergySystem:
    """
    Base Energy System class

    Parameters
    ----------
    nondispat : list
        List of non-dispatchable asset objects 
        i.e. loadAsset, pvAsset, hydroAsset, hpAsset

    dispat : list
        List of dispatchable assets. The order of which determines control
        strategy in basic energy balance.
        i.e. PracticalBatteryAsset

    dt : float
        time step

    T : float
        Number of time intervals
    """

    def __init__(self, nondispat, dispat, dt, T):
        self.nondispat = nondispat
        self.dispat = dispat
        self.assets = nondispat + dispat
        self.dt = dt  
        self.T = T    

    def basic_energy_balance(self):
        """
        Basic energy system balancing. Dispatchable assets are deployed in
        order defined by list.

        Returns
        -------

        net_load : Array
            The net load of the system.
        """
        nondispat = self.nondispat                              # nondispatchable asset list
        dispat = self.dispat                                    # dispatchable asset list


        # sum non-dispatchable assets
        net_nondis = np.zeros((self.T, 1))
        for i, asset in enumerate(nondispat):
            if asset.asset_type == 'DOMESTIC_LOAD':
                profile = nondispat[i].getOutput(self.dt)
            
            #elif asset.asset_type == 'HEAT_PUMP_LOAD': # waiting for steven
                #profile = nondispat[i].getOutput(self.dt)

            #elif asset.asset_type == 'EV_LOAD': # waiting for Minnie
                #profile = nondispat[i].getOutput(self.dt)
              
            elif asset.asset_type == 'NON_DOMESTIC_LOAD': 
                profile = nondispat[i].getOutput(self.dt)
               
            elif asset.asset_type == 'PV':
                profile = -1 * nondispat[i].getOutput(self.dt)  # -1 x generation asset

            elif asset.asset_type == 'SF':
                profile = -1 * nondispat[i].getOutput(self.dt)  # -1 x generation asset
               
            elif asset.asset_type == 'HYDRO':
                profile = -1 * nondispat[i].getOutput(self.dt)  # -1 x generation asset
             

            net_nondis = net_nondis + profile


        self.non_disp_load = net_nondis                         # returns net non-dispatchable load
        net_load = net_nondis


        # deploy dispatchable gen
        for i, asset in enumerate(dispat):
            profile = asset.getOutput(net_load)                 # surplus load is dispatched to the batteries
            net_load = net_load - profile


        self.net_load = net_load
        self.disp_load = net_load - net_nondis                  # returns net dispatachable load


        disp_load = self.disp_load
        non_disp_load = self.non_disp_load


        return net_load, disp_load, non_disp_load


def E_to_dailyE(data, dt):
    daily_sum = data.reshape(int(len(data)/(24/dt)), int(24/dt)).sum(axis=1)

    return daily_sum


if __name__ == "__main__":
    pass