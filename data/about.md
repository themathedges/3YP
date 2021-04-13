The data contained in OxEMF_3YP is example energy system data.

### solar02Jan.csv
Example winter day solar data obtained from [www.renewables.ninja](www.renewables.ninja).

Half hourly data, values are in kWh.

### wnt_wd.csv
Example weekday winter demand profile for the UK, obtained from [UKERC Energy Data Centre](http://ukerc.rl.ac.uk/cgi-bin/era001.pl?GoButton=EResult&STerm=elexon&SScope=&GoAct=&AFull=5&EWCompID=42&AllFilters=&RandKey=&TotHead=5%20results%20for%20%E2%80%9Celexon%E2%80%9D%20**)

Half hourly data, values are in kW.

### mip.csv
Example half hourly energy imbalance price from [Elexon](www.elexonportal.co.uk)

col 3: HH settlement period

col 4: System buy/sell price £/MWh

col 5: Net imbalance volume MWh

### ken_dom_annual_demand_per_household_3.csv
Half hourly power (kW) from domestic demand of an average household in Kennington over the period of one year.

### ken_non_dom_annual_demand_per_user_3.csv
Half hourly demand profile (kW) for an average non-domestic user in Kennington (eg a cafe, shop etc) 

### school_annual_demand.csv
Half hourly demand profile (kW) for an average (primary) school in Kennington (i.e. similar to non-domestic profile but zero demand at weekends and school holidays)

### EV_demand_night_1.csv
Half hourly demand profile (kW) for 40kWh battery Nissan Leaf. A smart charge point is used to largely limit the charging time to 11pm-5am 
(i.e. cheap night rates + low demand from uesrs, but also no solar generation at this time)

### EV_demand_day_1.csv
Half hourly demand profile (kW) for 40kWh battery Nissan Leaf. A smart charge point is used to largely limit the charging time to 9am-5pm 
(i.e. low demand from domestic users + it matches the peak generation times from solar)

### centralheatpump.csv 
Half hourly (kWh) annual demand profile for the central heat pump

### domestic_demand.csv
Half hourly annual demand profile (kWh) for the domestic electrification of gas for an average house in Kennington. Demand for space heating, hot water heating and cooking included.  

### nondomestic_demand.csv
Half hourly annual demand profile (kWh) for the total non-domestic electrification of gas in Kennington. 

### passivhaus_demand.csv
Half hourly annual demand profile (kWh) for a home built to Passivhaus standards, for new builds leading up to 2050. Demand for space heating, hot water heating and cooking included. 
