"""
Example 1: Analysing a single file with hydrodynamic output data.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
from examples.example_plot import create_figure
from src.processing import map_ecotopes

# map ecotopes based on hydrodynamic output data: 'file-name_map.nc'
results = map_ecotopes('file-name_map.nc', wd='directory/to/output/files')

# plot spatial distribution of ecotopes, i.e., an ecotope-map
create_figure(results)
