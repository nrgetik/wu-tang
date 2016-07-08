#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wu import Base, Locale, Observation


def validate(v, t):
    if t == float:
        try:
            return float(v)
        except ValueError:
            return None
    if t == str:
        if isinstance(v, str) and len(v) > 1 and "N/A" not in v:
            return v
        else:
            return None


def main():
    engine = create_engine("sqlite:///wu-tang.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    loc_obsvns = []
    csvd = os.path.normpath("./csv-tmp")
    for d in os.listdir(csvd):
        airport_icao = d
        new_loc = Locale(airport_icao=airport_icao)
        session.add(new_loc)
        session.commit()
        del loc_obsvns[:]
        for f in os.listdir(os.path.join(csvd, d)):
            date_local = f[:-4]
            with open(os.path.join(csvd, d, f)) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if "Time" in row[0]:
                        continue
                    loc_obsvns.append([" ".join((date_local, row[0]))] +
                                      [col for col in row[1:]])
        engine.execute(
            Observation.__table__.insert(),
            [{"datetime_local": datetime.strptime(row[0], "%Y-%m-%d %I:%M %p"),
              "temperature_f": validate(row[1], float),
              "dew_point_f": validate(row[2], float),
              "relative_humidity": validate(row[3], float),
              "sea_level_pressure_in": validate(row[4], float),
              "visibility_miles": validate(row[5], float),
              "wind_direction": validate(row[6], str),
              "wind_speed_mph": validate(row[7], float),
              "gust_speed_mph": validate(row[8], float),
              "precipitation_in": validate(row[9], float),
              "events": validate(row[10], str),
              "conditions": validate(row[11], str),
              "wind_dir_degrees": validate(row[12], float),
              "datetime_utc": datetime.strptime(row[13], "%Y-%m-%d %H:%M:%S"),
              "locale_airport_icao": airport_icao}
             for row in loc_obsvns]
        )

if __name__ == "__main__":
    main()
