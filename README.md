# Png-To-Map (OSM Raster)
This Tool converts unreferenced PNG images to OSM raster maps.

# Usage
1. Place your PNG files in the `input` directory.
2. Start the Webserver to georeference the PNG files:
   ```bash
   cd webclient
   npm start
   ```
3. Open your PNG and georeferece it
4. Download the config
5. Place it alongside your image
6. Run ```bash python3 src/main.py <working_directory> <input_image> <config_file>```
   - Example: `python3 src/main.py ./data/ ./my_image.png ./config.json`