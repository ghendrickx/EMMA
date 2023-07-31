"""
Example 5: Analysing a single file with hydrodynamic output data using a non-default configuration. This can either be
(1) a built-in configuration; or (2) a custom (partial) configuration. In case of a custom (partial) configuration, see
`config/emma.json` for the relevant key-words. When only part of the configuration-file is to be customised, an
incomplete custom configuration-file can be provided including only the key-words to be customised.

The configuration-file for reading the hydrodynamic output data can also be customised. Instead of using the key-worded
argument `f_eco_config`, use `f_map_config`. Note that the custom configuration-files (if multiple are used) are
expected in the same directory (i.e., `wd_config`).

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
from examples._example_plot import create_figure
from src.processing import map_ecotopes

# map ecotopes based on hydrodynamic output data: 'file-name_map.nc'
# > option 1: built-in configuration (ZES.1)
results = map_ecotopes(
    'file-name_map.nc', wd='directory/to/output/files',
    f_eco_config='zes1.json'
)

# # > option 2: custom configuration ('custom.json')
# results = map_ecotopes(
#     'file-name_map.nc', wd='directory/to/output/files',
#     f_eco_config='custom.json', wd_config='directory/to/configuration'
# )

# # > option 3: custom map-configuration ('custom-map.json')
# results = map_ecotopes(
#     'file-name_map.nc', wd='directory/to/output/files',
#     f_map_config='custom-map.json', wd_config='directory/to/configuration'
# )

# plot spatial distribution of ecotopes, i.e., an ecotope-map
create_figure(results)
