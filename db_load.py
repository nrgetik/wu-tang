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

    session.add(Locale(airport_icao="KJFK", city="New York", state="NY",
                       time_zone="EDT"))
    session.commit()

    # session.add(Observation())
    # session.commit()

if __name__ == "__main__":
    main()
