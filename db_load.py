#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from datetime import datetime
from math import exp
from math import sqrt
from sqlalchemy import create_engine

from wu import Base, Locale, Observation


def calc_relative_humidity(t, dp):
    return 100 * (exp((17.625 * dp) / (243.04 + dp)) /
                  exp((17.625 * t) / (243.04 + t)))


def calc_heat_index(t, rh):
    simple = 0.5 * (t + 61.0 + ((t - 68.0) * 1.2) + (rh * 0.094))
    if ((t + simple) / 2.0) < 80.0:
        return simple
    else:
        full = -42.379 + (2.04901523 * t) + (10.14333127 * rh) - \
            (0.22475541 * t * rh) - (0.00683783 * t * t) - \
            (0.05481717 * rh * rh) + (0.00122874 * t * t * rh) + \
            (0.00085282 * t * rh * rh) - (0.00000199 * t * t * rh * rh)
        if (rh < 13.0) and (80.0 <= t <= 112.0):
            return full - ((13.0 - rh) / 4.0) * \
                sqrt((17.0 - abs(t - 95.0)) / 17.0)
        elif (rh > 85.0) and (80.0 <= t <= 87.0):
            return full + ((rh - 85.0) / 10.0) * ((87.0 - t) / 5.0)
        else:
            return full


def validate_field(v, t):
    if t == float:
        try:
            val = round(float(v), 2)
            if val != -9999.0:
                return val
            else:
                return None
        except ValueError:
            return None
    if t == str:
        if isinstance(v, str) and len(v) > 1 and "N/A" not in v:
            return v
        else:
            return None


def main():
    engine = create_engine("sqlite:///wu-tang.db", echo=False)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    loc_obsvns = []
    csvd = os.path.normpath("./wg-csv")
    for d in sorted(os.listdir(csvd)):
        airport_icao = d
        with open("./airport-city-state.csv") as f:
            lines = f.readlines()
            line = [i for i, s in enumerate(lines) if airport_icao in s][0]
            city = lines[line].split(",")[1].strip()
            state = lines[line].split(",")[2].strip()
        engine.execute(
            Locale.__table__.insert(),
            {"airport_icao": airport_icao,
             "city": city,
             "state": state}
        )
        del loc_obsvns[:]
        for f in os.listdir(os.path.join(csvd, d)):
            date_local = f[:-4]
            with open(os.path.join(csvd, d, f)) as csvfile:
                reader = csv.reader(csvfile)
                time_zone = next(reader)[0][4:]
                for row in reader:
                    loc_obsvns.append([" ".join((date_local, row[0]))] +
                                      [col for col in row[1:]])
        for obs in loc_obsvns:
            obs[1] = validate_field(obs[1], float)
            obs[2] = validate_field(obs[2], float)
            obs[3] = validate_field(obs[3], float)
            if obs[1] and obs[2] and not obs[3]:
                obs[3] = validate_field(calc_relative_humidity(obs[1], obs[2]),
                                        float)
            if obs[1] and obs[3]:
                obs.append(validate_field(calc_heat_index(obs[1], obs[3]),
                                          float))
            else:
                obs.append(None)
        engine.execute(
            Observation.__table__.insert(),
            [{"datetime_local": datetime.strptime(row[0], "%Y-%m-%d %I:%M %p"),
              "time_zone": validate_field(time_zone, str),
              "temperature_f": row[1],
              "dew_point_f": row[2],
              "relative_humidity": row[3],
              "heat_index_f": row[14],
              # "sea_level_pressure_in": validate_field(row[4], float),
              # "visibility_miles": validate_field(row[5], float),
              # "wind_direction": validate_field(row[6], str),
              "wind_speed_mph": validate_field(row[7], float),
              "gust_speed_mph": validate_field(row[8], float),
              "precipitation_in": validate_field(row[9], float),
              "events": validate_field(row[10], str),
              "conditions": validate_field(row[11], str),
              # "wind_dir_degrees": validate_field(row[12], float),
              "datetime_utc": datetime.strptime(row[13], "%Y-%m-%d %H:%M:%S"),
              "locale_airport_icao": airport_icao}
             for row in loc_obsvns]
        )

if __name__ == "__main__":
    main()
