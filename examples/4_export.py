"""
Example 4: Analysing a single file with hydrodynamic output data, and export the ecotope-data to a `*.csv`-file. The
data is either exported (1) with the default file-name (`f_export=True`), or (2) with a custom file-name
(`f_export='custom-file-name'`).

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
from examples.example_plot import create_figure
from src.processing import map_ecotopes

# map ecotopes based on hydrodynamic output data: 'file-name_map.nc'
# > option 1: export with default file-name
results = map_ecotopes(
    'file-name_map.nc', wd='directory/to/output/files',
    f_export=True, wd_export='output/directory'
)

# # > option 2: specify custom output file-name (*.csv-file)
# results = map_ecotopes(
#     'file-name_map.nc', wd='directory/to/output/files',
#     f_export='custom-file-name', wd_export='output/directory'
# )

# plot spatial distribution of ecotopes, i.e., an ecotope-map
create_figure(results)
