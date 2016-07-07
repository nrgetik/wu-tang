#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from wu import Base, Locale, Observation


def main():
    engine = create_engine("sqlite:///wu-tang.db")
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
