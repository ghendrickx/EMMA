"""
Example 2: Analysing a multiple files with hydrodynamic output data in parallel.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
from examples.example_plot import create_figure
from src.processing import map_ecotopes

# map ecotopes based on hydrodynamic output data: 'file-name-0_map.nc', 'file-name-1_map.nc'
results = map_ecotopes(
    'file-name-0_map.nc', 'file-name-1_map.nc',
    wd='directory/to/output/files',
    n_cores=2
)

# plot spatial distribution of ecotopes, i.e., an ecotope-map
create_figure(results)
