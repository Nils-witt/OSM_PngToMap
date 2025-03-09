import math


# Credits: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    x_tile = (lon_deg + 180.0) / 360.0 * n
    y_tile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return x_tile, y_tile


# Credits: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
def num2deg(x_tile, y_tile, zoom):
    n = 1 << zoom
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg
