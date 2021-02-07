# 3YP Overall Energy System Model

## Non-Distpatchable Energy Assets In Kennington

### Sandford Hydro - hydroAsset
Dataset: data/Sandford_hydro_generation_30_min_date.csv
Peak power output = 440 kWp
Annual maintenance = £100,000
Number of installations = 1

<br />
### Domestic Solar PV Panels - pvAsset
Dataset: data/oxon_solar_2014.csv
Peak power output = 4 kWp
Annual maintenance = £100
Installation cost = £6,000
Number of installations = 1500 (number of houses in Kennington)

<br />
### Domestic Energy Demand - loadAsset
Dataset: data/oxon_class1_year_load.csv
Number of installations = 1700 (number of households in Kennington)

<br />
### Non-domestic Energy Demand - ndAsset
Dataset: ?

<br />
### Water Source Heat Pump System - hpAsset
Dataset: ?
Power input = ?
Annual maintenance = ?
Installation cost = ?
Number of installations = 1700 (number of households in Kennington)

<br />
<br />

## Dispatchable Energy Assets In Kennington

### Domestic Battery Storage - PracticalBatteryAsset1
Battery data: Nissan Leaf EV
Power capacity = 6.6 kW (standard wall charge)
Maximum storage capacity = 36 kWh
Efficiency = 70%
Annual maintenance = ?
Installation cost = £27,000 (Nissan Leaf EV)
Number of installations = 700 (50% of houses in Kennington owning at least one car)

<br />
### Community Battery - PracticalBatteryAsset2
Battery data: Nissan Leaf EV
Power capacity = 6.6 kW
Maximum storage capacity = 28.8 kWh (80% of original capacity)
Efficiency = 70%
Annual maintenance = ?
Installation cost = £500 (typical repurposed EV battery)
Number of installations = 200

<br />
### Octopus Energy Supplier - gridAsset

<br />
<br />

