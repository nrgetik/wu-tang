# wu-tang
Weather Underground [-based] Thermal/Atmospheric Niceness Grade

## description
This software seeks to determine the number of days that fall within certain
climate/weather parameters observed at select US airports, and thus their
corresponding cities, in an effort to rank atmospheric "niceness" amongst these
locales.

## specification
Limiting observations to (roughly) daytime/afternoon hours, the proposed
methodology is:

* Calculate days with a minimum temperature >= 42°F and a maximum temperature
  <= 97°F
* Subtract days with an average heat index >= 91°F (excludes
  dangerous/uncomfortable heat/humidity)
* Subtract days with significant precipitation (excludes inconvenient rainfall)
* Subtract days with significant cloud cover (excludes dreariness)
* Subtract days with low visibility (excludes fog/air pollution)

Snow fall/cover will not be considered as both should be irrelevant as a
consequence of the existing parameters.

## disclaimer
This software is not in any way associated with the commercial weather service
Weather Underground, its affiliates, or subsidiaries.
