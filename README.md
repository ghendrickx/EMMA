![Tests](https://github.com/ghendrickx/EMMA/actions/workflows/tests.yml/badge.svg)

# EMMA
The _Ecotope Map Maker based on Abiotics_ (EMMA) facilitates the translation from hydrodynamic model output data to 
ecotope maps. _Ecotopes_ are ecological units that are defined by abiotic, biotic, and anthropogenic local conditions.
An _ecotope_ is a more-or-less homogeneous natural unit. In many instances, the word _habitat_ is used where here the 
word _ecotope_ is used, as _habitat_ originally refers to the living environment of a single species, while _ecotope_ 
refers to an ecosystem as it can be mapped.

This simple `python`-interface allows to map ecotopes (or habitats) based on the abiotic output from an hydrodynamic 
model. It does so by a modified version of the [ZES.1](https://edepot.wur.nl/174540) classification system. The
hydrodynamic model must contain the following three hydrodynamic parameters:
 1. water depth (or, bottom and water level);
 1. flow velocity; and
 1. salinity.
 
Some basic usage of EMMA is presented below ([Basic usage](#basic-usage)). A more complete overview of use-cases are
grouped in the [examples](examples)-folder.

## Authors
Soesja Brunink
[![alt text](https://camo.githubusercontent.com/e1ec0e2167b22db46b0a5d60525c3e4a4f879590a04c370fef77e6a7e00eb234/68747470733a2f2f696e666f2e6f726369642e6f72672f77702d636f6e74656e742f75706c6f6164732f323031392f31312f6f726369645f31367831362e706e67) 0009-0007-4626-8909](https://orcid.org/0009-0007-4626-8909) 
(Arcadis).

Gijs G. Hendrickx 
[![alt text](https://camo.githubusercontent.com/e1ec0e2167b22db46b0a5d60525c3e4a4f879590a04c370fef77e6a7e00eb234/68747470733a2f2f696e666f2e6f726369642e6f72672f77702d636f6e74656e742f75706c6f6164732f323031392f31312f6f726369645f31367831362e706e67) 0000-0001-9523-7657](https://orcid.org/0000-0001-9523-7657)
(Delft University of Technology).

Contact: [G.G.Hendrickx@tudelft.nl](mailto:G.G.Hendrickx@tudelft.nl?subject=[GitHub]%20ANNESI: ).

## References
When using this repository, please cite accordingly:
>   Hendrickx, G.G., and 
    Brunink, S. 
    (2023). 
    EMMA: Ecotope-map maker based on abiotics.
    4TU.ResearchData.
    Software.
    doi: [10.4121/0100fc5a-a99c-4002-9864-3faade3899e3](https://doi.org/10.4121/0100fc5a-a99c-4002-9864-3faade3899e3).

## License
This repository is licensed under [`Apache License 2.0`](LICENSE).

## Requirements
This repository has the following requirements (see also [`requirements.txt`](requirements.txt)):
 -  `shapely`
 -  `numpy`
 -  `netCDF`

## Basic usage
The basic usage of `EMMA` requires calling the `map_ecotopes()`-function:
```python
from src.processing import map_ecotopes

dict_ecotopes = map_ecotopes('<hydrodynamic_output_data_file>.nc', wd='<working/directory>')
```
By default, `EMMA` expects the relevant variables to be named as stated by [`dfm2d.json`](config/dfm2d.json). In case
these key-words differ in the provided `netCDF`-file, provide a custom (partially overwriting) `*.json`-file with the
same key-words as in [`dfm2d.json`](config/dfm2d.json):
```python
from src.processing import map_ecotopes

dict_ecotopes = map_ecotopes(
    '<hydrodynamic_output_data_file>.nc', wd='<working/directory>',
    f_map_config='<map-configuration>.json'
)
```
where `<map-configuration>.json` is formatted as follows (see the built-in [`dfm2d.json`](config/dfm2d.json)):
```json
{
  "x-coordinates": "<key-word>",
  "y-coordinates": "<key-word>",
  "water-depth": "<key-word>",
  "x-velocity": "<key-word>",
  "y-velocity": "<key-word>",
  "salinity": "<key-word>",
  "depth-sign": "<+/->"
}
```
**Note** that the `depth-sign` key-word reflects the sign used to describe the water depth in the output map-file, which 
may be different from the direction of the `z`-axis. `"depth-sign": "+"` means that the water depth is defined as a 
positive value when the bottom is _**below**_ the reference level (e.g. mean sea level); and vice versa. 

**Note** that the tide-related key-words in the ecotope configuration file (e.g. [`emma.json`](config/emma.json)) 
consider the `z`-axis to be defined positive upwards. Thus, high water level is _**greater**_ than low water level.

In the [`examples`](examples)-folder, a collection of examples are provided on how to use `EMMA` including some of her 
additional features. A [dummy output-file](examples/ex_map_data) is added that can be used to test the examples. For the
examples, there is also an additional [`README`](examples/README.md) in the [`examples`](examples)-folder to provide
some background to the examples, where needed.

## Structure
The main features of `EMMA` is located in the [`src`](src)-directory, and the built-in configurations are grouped in the
[`config`](config)-directory:
```
+-- .github/
|   +-- workflows/
|   |   +-- tests.yml
+-- config/
|   +-- __init__.py
|   +-- config_file.py
|   +-- dfm2d.json
|   +-- emma.json
|   +-- zes1.json
+-- examples/
|   +-- ex_map_data/
|   |   +-- __init__.py
|   |   +-- output_map.nc
|   +-- 1_basic.py
|   +-- 2_parallel.py
|   +-- 3_settings.py
|   +-- 4_export.py
|   +-- 5_config.py
|   +-- __init__.py
|   +-- _example_plot.py
+-- src/
|   +-- __init__.py
|   +-- _globals.py
|   +-- export.py
|   +-- labelling.py
|   +-- performance.py
|   +-- preprocessing.py
|   +-- processing.py
+-- tests/
|   +-- __init__.py
|   +-- test_config.py
|   +-- test_labelling.py
|   +-- test_performance.py
|   +-- test_preprocessing.py
+-- .gitignore
+-- __init__.py
+-- LICENSE
+-- README.md
+-- requirements.txt
+-- setup.py
```
