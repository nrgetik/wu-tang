#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wu import Base, Locale, Observation


def main():
    engine = create_engine("sqlite:///wu-tang.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_locale = Locale(airport_icao="KJFK", city="New York", state="NY",
                        time_zone="EDT")
    session.add(new_locale)
    session.commit()

    new_observation = Observation(time_local=datetime.now(),
                                  date_utc=datetime.now(), temperature_f=55.5,
                                  dew_point_f=55.5, relative_humidity=55.5,
                                  sea_level_pressure_in=55.5,
                                  visibility_miles=55.5, wind_direction=55.5,
                                  wind_speed_mph=55.5, gust_speed_mph=55.5,
                                  precipitation_in=55.5, events="Thunderstorm",
                                  conditions="Scattered Clouds",
                                  wind_dir_degrees=55.5, locale=new_locale)
    session.add(new_observation)
    session.commit()

if __name__ == "__main__":
    main()
