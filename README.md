# 3YP Overall Energy System Model

## Non-Distpatchable Energy Assets In Kennington

### Sandford Hydro - hydroAsset
Dataset: data/Sandford_hydro_generation_30_min_date.csv
<br />
Power output = 450 kW
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
Number of installations = 1500 (number of houses in Kennington)

### Solar PV Farm - sfAsset
Dataset: data/oxon_solar_2014.csv ???
<br />
Peak power output = 4 kWp ???
<br />
Annual maintenance = £100 ???
<br />
Installation cost = £6,000 ???
<br />
Number of panels = ???

### Domestic Electricity Demand - loadAsset
Dataset: data/oxon_class1_year_load.csv
<br />
Number of installations = 1700 (number of households in Kennington)

### Non-Domestic Electricity Demand - ndAsset
Dataset: ?

### Electric Vehicle Electricity Demand - evAsset
Dataset: ?

### Water-Source Heat Pump System - hpAsset
Dataset: ?
<br />
Power input = ?
<br />
Annual maintenance = ?
<br />
Installation cost = ?
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
octopus_outgoing_2018_SE.csv : 2018 data for Octopus Outgoing tariff (pence/kWh) for the South East of UK. Data obtained from <a href="https://octopus.energy/blog/outgoing/">Octopus outgoing</a>
