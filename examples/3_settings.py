"""
Example 3: Analysing a single file with hydrodynamic output data with more accurate results by providing additional
information about the modelled area:
 -  `substratum_1`: The substratum in the area is either 'soft' or 'hard'.
 -  Tidal characteristics:
     *  `mlws`: Mean-Low-Water-Spring-tide, the MLWS representative for the area.
     *  `mhwn`: Mean-High-Water-Neap-tide, the MHWN representative for the area.
     *  `lat` : Lowest-Astronomical-Tide, the LAT representative for the area, which is used with the default ecotope-
                configuration: 'emma.json'. When not specified, it defaults to `mlws`.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
from examples._example_plot import create_figure
from src.processing import map_ecotopes

# map ecotopes based on hydrodynamic output data: 'file-name_map.nc'
results = map_ecotopes(
    'file-name_map.nc', wd='directory/to/output/files',
    substratum_1='soft', mlws=-2.31, mhwn=1.85, lat=-2.7
)

# plot spatial distribution of ecotopes, i.e., an ecotope-map
create_figure(results)
