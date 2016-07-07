#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt


def heat_index(t, rh):
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

#print(heat_index(90.0, 90.0))
