from create_basemap_image import generate_osm_png


def main():
    x_max = 34073
    x_min = 34057
    y_max = 22027
    y_min = 22011

    tile_url = "https://sgx.geodatenzentrum.de/wmts_basemapde/tile/1.0.0/de_basemapde_web_raster_farbe/default/GLOBAL_WEBMERCATOR/{z}/{y}/{x}.png"
    img = generate_osm_png(tile_url, x_min, x_max, y_min, y_max, 16)
    #img = generate_osm_png(tile_url, x_min, x_min, y_min, y_min, 16)
    img.save("tmp/basemap.png")

if __name__ == "__main__":
    main()