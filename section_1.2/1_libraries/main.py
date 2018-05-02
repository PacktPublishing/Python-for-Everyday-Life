# -*- coding: utf-8 -*-
# !/usr/bin/env python3

if __name__ == '__main__':
    import geopoints

    nowhere = (765.1, -445.8)
    london = (-0.15, 51.51)
    quito = (-78.4, 0.0)
    perth = (-31.95, 115.86)

    print(geopoints.is_geopoint(*nowhere))
    print(geopoints.is_in_northern_emisphere(*quito))
    print(geopoints.is_on_equator(*quito))
    print(geopoints.is_in_southern_emisphere(*quito))