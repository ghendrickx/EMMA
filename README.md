![Tests](https://github.com/ghendrickx/EMMA/actions/workflows/tests.yml/badge.svg)

# EMMA
The _Ecotope Map Maker based on Abiotics_ (EMMA) facilitates the translation from hydrodynamic model output data to 
ecotope maps. _Ecotopes_ are ecological units that are defined by abiotic, biotic, and anthropogenic local conditions.
An _ecotope_ is a more-or-less homogeneous natural unit. In many instances, the word _habitat_ is used where here the 
word _ecotope_ is used, as _habitat_ originally refers to the living environment of a single species, while _ecotope_ 
refers to an ecosystem as it can be mapped.

This simple `python`-interface allows to map ecotopes (or habitats) based on the abiotic output from an hydrodynamic 
model. It does so by a modified version of the [ZES.1](https://edepot.wur.nl/174540) classification system. The
hydrodynamic model must contain the following hydrodynamic parameters:
-   water depth (and level);
-   flow velocity; and
-   salinity.

## Authors
Soesja Brunink (Arcadis).

Gijs G. Hendrickx 
[![alt text](https://camo.githubusercontent.com/e1ec0e2167b22db46b0a5d60525c3e4a4f879590a04c370fef77e6a7e00eb234/68747470733a2f2f696e666f2e6f726369642e6f72672f77702d636f6e74656e742f75706c6f6164732f323031392f31312f6f726369645f31367831362e706e67) 0000-0001-9523-7657](https://orcid.org/0000-0001-9523-7657)
(Delft University of Technology).

Contact: [G.G.Hendrickx@tudelft.nl](mailto:G.G.Hendrickx@tudelft.nl?subject=[GitHub]%20ANNESI: ).

## Requirements
This repository has the following requirements (see also [`requirements.txt`](requirements.txt)):
- `numpy>=1.19.4`
- `netCDF>=1.5.7`

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
where `<map-configuration>.json` is formatted as follows (e.g., see the built-in [`dfm2d.json`](config/dfm2d.json)):
```json
{
  "x-coordinates": "<key-word>",
  "y-coordinates": "<key-word>",
  "water-depth": "<key-word>",
  "x-velocity": "<key-word>",
  "y-velocity": "<key-word>",
  "salinity": "<key-word>",
  "z-direction": "<up/down>"
}
```

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
+-- src/
|   +-- __init__.py
|   +-- export.py
|   +-- labelling.py
|   +-- performance.py
|   +-- preprocessing.py
|   +-- processing.py
+-- tests/
|   +-- __init__.py
|   +-- test_config.py
|   +-- test_labelling.py
|   +-- test_preprocessing.py
+-- .gitignore
+-- LICENSE
+-- README.md
+-- requirements.txt
```

## License
This repository is licensed under [`Apache License 2.0`](LICENSE).
