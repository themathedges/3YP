#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3YP basic market module.
Authors: Avinash Vijay, Scot Wheeler
"""

__version__ = "0.4"

import pandas as pd
import numpy as np
import datetime


class marketObject():
    """
    Market class for calculating energy price.
    """
    def __init__(self, system,
                 startDate=datetime.datetime(2017, 1, 1),
                 endDate=datetime.datetime(2017, 12, 31, 23, 59, 59),
                 export_rate=5.24):
        
        self.system = system
        self.bill_fact = 0.33  # percentage of bill related to energy
        
        self.mip = self.getMipRates(startDate, endDate).values / 10  # convert £/mWh to p/kWh
        self.mip /= self.bill_fact
        self.export_rate = export_rate

    def getMipRates(self, startDate, endDate):
        """
        Import market imbalance price, fill missing data with NaN, crop to
        period of interest.

        Parameters
        ----------
        startDate : datetime
            Start of period of interest.
        endDate : datetime
            End of period of interest.

        Returns
        -------
        apxData : DataFrame
            Import market imbalance price (£/MWh).

        """
        data1 = pd.read_csv('data/sspsbpniv.csv', index_col=0,
                            parse_dates=True)
        start = data1.index[0]
        new_index = pd.date_range(start=start, periods=len(data1), freq='0.5H')
        
        data1.set_index(new_index, inplace=True)
        apxData = pd.DataFrame(
                data1.loc[startDate:endDate, "System Buy Price(£/MWh)"])
        return apxData

    def getGridCost(self):
        """
        Calculate import/export payments for net electricity, including
        export rate.

        Returns
        -------
        Total cost
        """
        net_load = self.system.net_load

        import_E = net_load >= 0
        export_E = net_load < 0
        cost_profile = np.zeros((len(net_load),1))
        cost_profile[import_E] = self.mip[import_E]
        cost_profile[export_E] = self.export_rate
        cost = net_load * cost_profile
        self.grid_cost = cost
        return cost

    def getFiTGenCost(self):
        """
        Calculate generation FiT contribution
        Fit generation rate set in asset.
        """
        FitGen_profile = np.zeros((len(self.system.net_load),1))
        for asset in self.system.assets:
            asset_FiTGen = asset.output * asset.genFiT
            FitGen_profile += asset_FiTGen
        self.genFiT = FitGen_profile
        return FitGen_profile

    def getInstallCost(self):
        """
        Total install cost of system.
        Install cost and expected lifetime set in asset.
        """
        total_install_cost = 0
        total_per_year_life = 0
        for asset in self.system.assets:
            total_install_cost += (asset.install_cost * asset.capacity)
            total_per_year_life += ((asset.install_cost * asset.capacity)
                                    / asset.lifetime)

        return total_install_cost, total_per_year_life

    def getTotalCost(self):
        """
        Total system cost. Grid + FiT gen + installation
        """
        total_cost = (self.getGridCost().sum()
                      - self.getFiTGenCost().sum()
                      + self.getInstallCost()[1])
        return total_cost

    def gridBreakdown(self):
        """
        Separate import and export payment
        """
        net_load = self.system.net_load
        grid_cost = self.getGridCost()
        purchased = np.zeros((len(net_load),1))
        sold = np.zeros((len(net_load),1))
        purchased[grid_cost >= 0] = grid_cost[grid_cost >= 0]
        sold[grid_cost < 0] = grid_cost[grid_cost < 0]
        return purchased, sold


if __name__ == "__main__":
    price = marketObject(None, datetime.datetime(2017, 1, 1),
                         datetime.datetime(2017, 12, 31, 23, 59, 59)).mip
