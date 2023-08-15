# EMMA: Examples
Five examples have been included to aid in the usage of `EMMA`:
 1. **Basic, single-file usage.**
    The most basic usage of `EMMA` using a single map-file.
 
 1. **Parallel, multi-file usage.**
    Parallel usage of `EMMA` using multiple map-files.
 
 1. **Added physical data.**
    Improved accuracy of `EMMA` by providing additional data, such as tidal characteristics.
 
 1. **Export output data.**
    Export the ecotope-map determined by `EMMA` to a `*.csv`-file.
 
 1. **Customising configurations.**
    Customising the configuration of the ecotope-labels and/or the keywords in the hydrodynamic output data. This means
    overwriting (part of) the configurations files (i.e., the `*.json`-files in the [`config`](../config)-folder).
    
All examples make use of a basic [plot-function](_example_plot.py) to visualise the results. This function can also be
used as a starting point for visualising the ecotope-maps.

To work with the examples, a [dummy output-file](ex_map_data) is included in this folder. **Note** that for the
_parallel, multi-file usage_-example, there is no enhanced computation time for single-file usage due to the 
implementation of parallel computing, which is file-based. Nevertheless, the use-case described in 
[_parallel, multi-file usage_](2_parallel.py) also works with a single map-file.
