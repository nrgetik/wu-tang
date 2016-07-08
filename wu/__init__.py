#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Locale(Base):
    __tablename__ = "locales"
    id = Column(Integer, primary_key=True)
    airport_icao = Column(String, index=True, nullable=False)
    city = Column(String)
    state = Column(String)
    time_zone = Column(String)


class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True)
    datetime_local = Column(DateTime, index=True, nullable=False)
    temperature_f = Column(Float)
    dew_point_f = Column(Float)
    relative_humidity = Column(Float)
    sea_level_pressure_in = Column(Float)
    visibility_miles = Column(Float)
    wind_direction = Column(String)
    wind_speed_mph = Column(Float)
    gust_speed_mph = Column(Float)
    precipitation_in = Column(Float)
    events = Column(String)
    conditions = Column(String)
    wind_dir_degrees = Column(Integer)
    datetime_utc = Column(DateTime, nullable=False)
    locale_id = Column(Integer, ForeignKey("locales.id"))
    locale = relationship(Locale)
