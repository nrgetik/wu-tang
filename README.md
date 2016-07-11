# wu-tang
Weather Underground [-based] Thermal/Atmospheric Niceness Grade

## description
This software seeks to determine the number of days that fall within certain
climate/weather parameters observed at select US airports, and thus their
corresponding cities, in an effort to rank atmospheric "niceness" amongst these
locales.

## specification
Limiting observations to roughly daytime/afternoon hours (1200-1800), the proposed
methodology is:

* Calculate days with a minimum temperature >= 42°F and a maximum temperature
  <= 98°F
* Subtract days with an average heat index >= 91°F (controls for
  dangerous/uncomfortable heat/humidity)
* Subtract days with significant precipitation (controls for inconvenient
  rain/snow fall)
* Subtract days with significant cloud cover (controls for dreariness)
* Subtract days with low visibility (controls for haze/smog)
* Factor in wind speed according to Beaufort scale

## disclaimer
This software is not in any way associated with the commercial weather service
Weather Underground, its affiliates, or subsidiaries.
