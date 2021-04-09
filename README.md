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
Number of installations = 100 (2020), 400 (2050)


### Solar PV Farm - sfAsset
Peak power output = ???
<br />
Annual maintenance = ??? 
<br />
Installation cost = ???
<br />
Number of panels = 30,000


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
<br />
Number of installations = 1700 (number of households in Kennington)


### Shoebox Heat Pump Systems - shoeAsset


### Shoebox Heat Pump Systems - ndShoeAsset


<br />

## Dispatchable Energy Assets In Kennington

### Domestic Battery Storage - PracticalBatteryAsset1
Battery data: Nissan Leaf EV
<br />
Power capacity = 6.6 kW (standard wall charge)
<br />
Maximum storage capacity = 40 kWh
<br />
Efficiency = 80%
<br />
Annual maintenance = ?
<br />
Installation cost = £27,000 (Nissan Leaf EV)
<br />
Number of installations = 700 (50% of houses in Kennington owning at least one car)


### Community Battery - PracticalBatteryAsset2
Battery data: Nissan Leaf EV
<br />
Power capacity = 6.6 kW
<br />
Maximum storage capacity = 28.8 kWh (80% of original capacity)
<br />
Efficiency = 70%
<br />
Annual maintenance = ?
<br />
Installation cost = £500 (typical repurposed EV battery)
<br />
Number of installations = 200

<br />

## Datasets

### Sandford Hydro
Sandford_hydro_generation_30_min_date.csv : 2020 generation from 
gen_2050_export_df_v1.csv : 2050 generation predicted from linear regression model

### Solar
oxon_solar_2014.csv : 2014 generation per typical 4 kW installation

### Heat Pump
centralheatpump.csv : central heat pump load
domestic_demand.csv : domestic heat pump load per house
nondomestic_demand.csv : non-domestic heat pump load per user

### Loads
EV_demand1 : EV load per vehicle
ken_dom_annual_demand_per_household_2 : 2020 domestic load per house
ideal_domestic_demand_per_household_v1 : 2050 domestic load per house predicted from
ken_non_dom_annual_demand_per_user : non_domestic load per user

### Storage
EV Batteries
Community Batteries
Domestic Storage Batteries

### Outgoing Tariff
octopus_outgoing_2018_SE.csv : 2018 data for Octopus Outgoing tariff (pence/kWh) for the South East of UK. Data obtained from <a href="https://octopus.energy/blog/outgoing/">Octopus Outgoing</a>

### Carbon Intensity
Carbon_Intensity_Data_*Month*.csv : 2020 data for the carbon intensity of emissions for the whole UK. Data obtained from <a href="https://carbonintensity.org.uk/">Carbon Intensity API</a>
