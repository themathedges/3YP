# 3YP Overall Energy System Model

## Non-Distpatchable Energy Assets In Kennington

### Sandford Hydro - hydroAsset
Peak power output = 450 kWp
<br />
Annual maintenance = £100,000
<br />
Number of installations = 1


### Domestic Solar PV Panels - pvAsset
Peak power output = 4 kWp
<br />
Annual maintenance = £100
<br />
Installation cost = £6,000
<br />
Number of installations = 2.8% of households (2020), 100% of households (2050)


### Solar PV Farm - sfAsset
Peak power output = 20 MW
<br />
Annual maintenance = ??? 
<br />
Installation cost = ???
<br />
Number of panels = 45,000


### Domestic Electricity Demand - loadAsset
Number of households = 1985 (2020), 2574 (2050)


### Non-Domestic Electricity Demand - ndAsset
Number of businesses = 36 (2020), 46 (2050)


### Electric Vehicle Electricity Demand - evAsset
Number of cars = 1 (2020), 3599 (2050)


### Central Water-Source Heat Pump System - hpAsset
Peak power input = ???
<br />
Annual maintenance = ???
<br />
Installation cost = ???


### Shoebox Heat Pump Systems - hpAsset
Number of installations = number of households


### Shoebox Heat Pump Systems - hpAsset
Number of installations = number of businesses


<br />

## Dispatchable Energy Assets In Kennington

### Domestic Battery Storage - PracticalBatteryAsset1
Battery data: Nissan Leaf EV
<br />
Power capacity = 50 kW (rapid charge)
<br />
Maximum storage capacity = 32 kWh (80% of original)
<br />
Efficiency = 80%
<br />
Annual maintenance = ???
<br />
Installation cost = ???
<br />
Number of installations = number of households with PV


### Community Battery - PracticalBatteryAsset2
Battery data: Tesla Powerpack 2
<br />
Power capacity = 500 kW
<br />
Maximum storage capacity = 4.2 MWh
<br />
Efficiency = 100%
<br />
Annual maintenance = ???
<br />
Installation cost = ???


### V2G - PracticalBatteryAsset3
Battery data: Nissan Leaf EV
<br />
Power capacity = 50 kW (rapid charge)
<br />
Maximum storage capacity = 40 kWh
<br />
Efficiency = 100%
<br />
Annual maintenance = ???
<br />
Installation cost = £27,000 (Nissan Leaf EV)
<br />
Number of installations = number of households with EV


<br />

## Datasets

### Sandford Hydro
Sandford_hydro_generation_30_min_date.csv : 2020 generation from 
gen_2050_export_df_v1.csv : 2050 generation predicted from linear regression model

### Solar
oxon_solar_2014.csv : 2014 generation in kW/kWp

### Heat Pump
centralheatpump.csv : central heat pump load
domestic_demand.csv : domestic heat pump load per house
nondomestic_demand.csv : non-domestic heat pump load per user
passivhaus_demand.csv : future heating demand of future new builds

### Loads
EV_Demand_day_1.csv : EV load per vehicle during daytime
EV_demand_night_1.csv : EV load per vehicle during nighttime
ken_dom_annual_demand_per_household_2.csv : 2020 domestic load per house
ideal_domestic_demand_per_household_v1.csv : 2050 domestic load per house predicted from
ken_non_dom_annual_demand_per_user.csv : non_domestic load per user

### Storage
Nissan Leaf : EV Batteries 
Tesla Powerpack 2 : Community Battery
Nissan Leaf at 80% efficiency and capacity : Domestic Storage Batteries

### Outgoing Tariff
octopus_outgoing_2018_SE.csv : 2018 data for Octopus Outgoing tariff (pence/kWh) for the South East of UK. Data obtained from <a href="https://octopus.energy/blog/outgoing/">Octopus Outgoing</a>

### Carbon Intensity
Carbon_Intensity_Data_*Month*.csv : 2020 data for the carbon intensity of emissions for the whole UK. Data obtained from <a href="https://carbonintensity.org.uk/">Carbon Intensity API</a>
