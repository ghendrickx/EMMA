![Tests](https://github.com/ghendrickx/EMMA/actions/workflows/tests.yml/badge.svg)

# EMMA
The _Ecotope-Map Maker based on Abiotics_ (EMMA) facilitates the translation from hydrodynamic model output data to 
ecotope maps. _Ecotopes_ are ecological units that are defined by abiotic, biotic, and anthropogenic local conditions.
An _ecotope_ is a more-or-less homogeneous natural unit. In many instances, the word _habitat_ is used where here the 
word _ecotope_ is used, as _habitat_ originally refers to the living environment of a single species, while _ecotope_ 
refers to an ecosystem as it can be mapped.

This simple `python`-interface allows to map aquatic ecotopes (or habitats) based on the abiotic output from an 
hydrodynamic model. It does so by a modified version of the [ZES.1](https://edepot.wur.nl/174540) classification system. 
The hydrodynamic model must contain the following three hydrodynamic parameters:
 1. water depth (or, bottom and water level);
 1. flow velocity; and
 1. salinity.
 
Some basic usage of `EMMA` is presented below ([Basic usage](#basic-usage)). A more complete overview of use-cases are
grouped in the [examples](examples)-folder.

## Authors
Gijs G. Hendrickx 
[<img src=https://info.orcid.org/wp-content/uploads/2020/12/orcid_16x16.gif alt="ORCiD" width="16" height="16">](https://orcid.org/0000-0001-9523-7657)
(Delft University of Technology).

Soesja Brunink
[<img src=https://info.orcid.org/wp-content/uploads/2020/12/orcid_16x16.gif alt="ORCiD" width="16" height="16">](https://orcid.org/0009-0007-4626-8909) 
(Arcadis).

Contact: [G.G.Hendrickx@tudelft.nl](mailto:G.G.Hendrickx@tudelft.nl?subject=[GitHub]%20EMMA:%20).

## References
When using this repository, please cite accordingly:
>   Hendrickx, G.G., and 
    Brunink, S. 
    (2023). 
    EMMA: Ecotope-Map Maker based on Abiotics.
    4TU.ResearchData.
    Software.
    doi: [10.4121/0100fc5a-a99c-4002-9864-3faade3899e3](https://doi.org/10.4121/0100fc5a-a99c-4002-9864-3faade3899e3).

## License
This repository is licensed under [`Apache License 2.0`](LICENSE).

## Installation
This repository has the following requirements (see also [`requirements.txt`](requirements.txt)):
 -  `Python>=3.9.0`
 -  `netCDF4`
 -  `numpy`
 -  `shapely`
 -  `typer`
 -  `xarray`

Instead of installing `netCDF4`, the `xarray`-package can also be installed with the `I/O`-option enabled:
```
python3 -m pip install "xarray[io]"
```
For further details, see the 
[`xarray`-documentation](https://docs.xarray.dev/en/stable/getting-started-guide/installing.html#instructions);
also for further details on installing `xarray`.

As of now, `EMMA` is not available via `PyPI` and can only be installed via `GitHub`. Below, there are three ways 
presented on how to install `EMMA` via `GitHub`. All these methods require you to have your virtual environment 
activated. If you have no virtual environment yet, consider creating one 
([official documentation](https://docs.python.org/3/library/venv.html)):
```
python3 -m venv <venv>
```

### Install directly
`EMMA` can be installed using `pip` directly:
 1. Install `EMMA`-repository using its `HTTPS`-hyperlink:
    ```
    python3 -m pip install git+https://github.com/ghendrickx/EMMA.git
    ```

### Clone repository
`EMMA` can be cloned according to the 
[`GitHub`-instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
(note that you need to have `git` on your computer):
 1. Open the command-line (or `Git Bash` on Windows), and change the directory to the desired location (using `cd`)
 1. Clone the repository by typing `git clone` followed by `EMMA`'s `HTTPS`-hyperlink:
    ```
    git clone https://github.com/ghendrickx/EMMA.git
    ```
 1. Locally install `EMMA`:
    ```
    python3 -m pip install .
    ```
    Or, when storing `EMMA` at a different location from the virtual environment:
    ```
    python3 -m pip install /path/to/EMMA
    ```

### Download `ZIP`
`EMMA` can be downloaded as a `ZIP`-file and unpacked locally:
 1. Click on the `Code`-button on the [main page](https://github.com/ghendrickx/EMMA) and choose the 
 `Download ZIP`-option
 1. Check your `Downloads`-folder and extract the downloaded `ZIP`-file (`EMMA-master.zip`)
 1. Move the repository-folder to the desired location [optional]
 1. Locally install `EMMA`:
    ```
    python3 -m pip install .
    ```
    Or, when storing `EMMA` at a different location from the virtual environment:
    ```
    python3 -m pip install /path/to/EMMA
    ```


## Basic usage
The basic usage of `EMMA` requires calling the `map_ecotopes()`-function:
```python
from src.processing import map_ecotopes

results = map_ecotopes('<hydrodynamic_output_data_file>.nc', wd='<working/directory>')
```
There is also the option to use `EMMA` from the command line directly:
```commandline
emma run hydrodynamic_output_data_file.nc --wd working/directory
```
**Note** that the latter usage provides limited customisation. Call for the included features:
```commandline
emma run --help
```
By default, `EMMA` expects the relevant hydrodynamic variables to be named as given by [`dfm1.json`](config/dfm1.json). 
In case these key-words differ in the provided `netCDF`-file (dependent on the hydrodynamic modelling software used), 
provide a custom (partially overwriting) `*.json`-file with the same key-words as in [`dfm1.json`](config/dfm1.json); 
see the [`config`](config)-folder for an elaborate explanation on how to customise the configuration of `EMMA`.

In the [`examples`](examples)-folder, a collection of examples are provided on how to use `EMMA` including some of her 
additional features. A [dummy output-file](examples/ex_map_data) is added that can be used to test the examples. For the
examples, there is also an additional [`README`](examples/README.md) in the [`examples`](examples)-folder to provide
some background to the examples, where needed.
**Note** that these examples all make use of the `Python`-based execution of `EMMA`.
