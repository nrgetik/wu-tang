#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from wu import Base, Locale, Observation

engine = create_engine("sqlite:///wu-tang.db")

Base.metadata.create_all(engine)
