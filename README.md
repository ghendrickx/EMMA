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
Gijs G. Hendrickx 
[![alt text](https://camo.githubusercontent.com/e1ec0e2167b22db46b0a5d60525c3e4a4f879590a04c370fef77e6a7e00eb234/68747470733a2f2f696e666f2e6f726369642e6f72672f77702d636f6e74656e742f75706c6f6164732f323031392f31312f6f726369645f31367831362e706e67) 0000-0001-9523-7657](https://orcid.org/0000-0001-9523-7657)
(Delft University of Technology).

Soesja Brunink
[![alt text](https://camo.githubusercontent.com/e1ec0e2167b22db46b0a5d60525c3e4a4f879590a04c370fef77e6a7e00eb234/68747470733a2f2f696e666f2e6f726369642e6f72672f77702d636f6e74656e742f75706c6f6164732f323031392f31312f6f726369645f31367831362e706e67) 0009-0007-4626-8909](https://orcid.org/0009-0007-4626-8909) 
(Arcadis).

Contact: [G.G.Hendrickx@tudelft.nl](mailto:G.G.Hendrickx@tudelft.nl?subject=[GitHub]%20EMMA:%20).

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
 -  `numpy`
 -  `shapely`
 -  `xarray`

## Basic usage
The basic usage of `EMMA` requires calling the `map_ecotopes()`-function:
```python
from src.processing import map_ecotopes

dict_ecotopes = map_ecotopes('<hydrodynamic_output_data_file>.nc', wd='<working/directory>')
```
By default, `EMMA` expects the relevant variables to be named as stated by [`dfm4.json`](config/dfm4.json). In case
these key-words differ in the provided `netCDF`-file, provide a custom (partially overwriting) `*.json`-file with the
same key-words as in [`dfm4.json`](config/dfm4.json); see [`config`](config) for more information how to do so.

In the [`examples`](examples)-folder, a collection of examples are provided on how to use `EMMA` including some of her 
additional features. A [dummy output-file](examples/ex_map_data) is added that can be used to test the examples. For the
examples, there is also an additional [`README`](examples/README.md) in the [`examples`](examples)-folder to provide
some background to the examples, where needed.
