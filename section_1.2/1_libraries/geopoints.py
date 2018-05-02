# -*- coding: utf-8 -*-
# !/usr/bin/env python3

def is_geopoint(lon, lat):
    assert type(lon) is float, "lon must be a float"
    assert type(lat) is float, "'lat' must be a float"
    if lon < -180.0 or lon > 180.0:
        return False
    if lat < -90.0 or lat > 90.0:
        return False
    return True


def is_in_northern_emisphere(lon, lat):
    if not is_geopoint(lon, lat):
        raise ValueError('Invalid geopoint')
    return True if lat > 0 else False


def is_on_equator(lon, lat):
    if not is_geopoint(lon, lat):
        raise ValueError('Invalid geopoint')
    return True if lat == 0 else False


def is_in_southern_emisphere(lon, lat):
    if not is_geopoint(lon, lat):
        raise ValueError('Invalid geopoint')
    return True if lat < 0 else False