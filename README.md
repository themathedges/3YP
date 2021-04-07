# 3YP Overall Energy System Model

## Non-Distpatchable Energy Assets In Kennington

### Sandford Hydro - hydroAsset
Dataset: data/Sandford_hydro_generation_30_min_date.csv
<br />
Power output = 450 kWp
<br />
Annual maintenance = £100,000
<br />
Number of installations = 1

### Domestic Solar PV Panels - pvAsset
Dataset: data/oxon_solar_2014.csv
<br />
Peak power output = 4 kWp
<br />
Annual maintenance = £100
<br />
Installation cost = £6,000
<br />
Number of installations = 200-800

### Solar PV Farm - sfAsset
Dataset: data/oxon_solar_2014.csv 
<br />
Peak power output = 400 W 
<br />
Annual maintenance = £100 
<br />
Installation cost = ???
<br />
Number of panels = 30,000

### Domestic Electricity Demand - loadAsset
Dataset: data/ken_dom_annual_demand_per_household.csv
<br />
Number of installations = 1728 (number of households in Kennington in 2020)

Ideal Kennington demand per household (after shifting and reduction): data/ideal_domestic_demand_per_household_v1.csv

### Non-Domestic Electricity Demand - ndAsset
Dataset: data/ken_non_dom_annual_demand_per_user.csv
<br />
Number of Businesses = 36 (number of non-domestic businesses in Kennington in 2020 ~ mainly shops, cafes)

### Electric Vehicle Electricity Demand - evAsset
Dataset: ?

### Water-Source Heat Pump System - hpAsset
Dataset: data/centralheatpump.csv
<br />
Power input = ???
<br />
Annual maintenance = ???
<br />
Installation cost = ???
<br />
Number of installations = 1700 (number of households in Kennington)

<br />

## Dispatchable Energy Assets In Kennington

### Domestic Battery Storage - PracticalBatteryAsset1
Battery data: Nissan Leaf EV
<br />
Power capacity = 6.6 kW (standard wall charge)
<br />
Maximum storage capacity = 36 kWh
<br />
Efficiency = 70%
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

### Octopus Energy Supplier - gridAsset

<br />

## Datasets

### Sandford Hydro
gen_2050_export_df_v1.csv : version 1 of 2050 Sandford Hydro Generation Data predicted from linear regression model

### Outgoing Tariff
octopus_outgoing_2018_SE.csv : 2018 data for Octopus Outgoing tariff (pence/kWh) for the South East of UK. Data obtained from <a href="https://octopus.energy/blog/outgoing/">Octopus Outgoing</a>

### Carbon Intensity
Carbon_Intensity_Data_*Month*.csv : 2020 data for the carbon intensity of emissions for the whole UK. Data obtained from <a href="https://carbonintensity.org.uk/">Carbon Intensity API</a>
