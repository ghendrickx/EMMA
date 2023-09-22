# EMMA configurations
EMMA uses two types of configuration files:
 1. Ecotope-configuration file;
 1. Map-configuration file.

EMMA comes with some built-in configuration files (see [Built-in configurations](#built-in-configurations)), but also
except custom configuration files (see [Custom configurations](#custom-configurations)).

## Built-in configurations
Both types have built-in options, aside from their default configuration files:

**Ecotope-configuration files:**
 1. [`emma.json`](emma.json) (default)
 1. [`zes1.json`](zes1.json)

**Map-configuration files:**
 1. [`dfm4.json`](dfm4.json) (default)
 1. [`dfm1.json`](dfm1.json)
    
These built-in configuration files can be used by providing their names to their respective key-worded arguments when
calling the [`map_ecotopes()`](../src/processing.py)-method:
```python
from src.processing import map_ecotopes

results = map_ecotopes(
    'file-name_map.nc', wd='directory/to/output/files',
    f_eco_config='zes1.json',  # built-in ecotope configuration file
    f_map_config='dfm1.json',  # built-in map configuration file
)
```

Suggestions for other built-in configuration files can be proposed by reaching out to
[G.G.Hendrickx@tudelft.nl](mailto:G.G.Hendrickx@tudelft.nl?subject=[GitHub]%20EMMA:%20Built-in%20configuration-file).
**Note** that a proposed configuration file should comply with the guidelines provided for the custom configurations,
i.e., they should be correctly formatted (see [Custom configurations](#custom-configurations)).

## Custom configurations
Any custom configuration file must comply with the key-words as in the built-in configuration files, and only the values
should be modified.

**Note** that the configuration-file is expected in the same folder as from which the code is executed. Therefore, also 
provide the working directory of the configuration-file(s) using the optional argument `wd_config`. Keep in mind that in
case multiple custom configuration files are used, they must be placed in the same working directory (i.e., 
`wd_config`):
```python
from src.processing import map_ecotopes

results = map_ecotopes(
    'file-name_map.nc', wd='directory/to/output/files',
    f_eco_config='custom_eco.json',  # custom ecotope configuration file
    f_map_config='custom_map.json',  # custom map configuration file
    wd_config='directory/to/configuration/files',  # working directory with custom configuration file(s)
)
```

### Ecotope-configuration file
The ecotope-configuration file follows the structure of the ecotope-labels and defines the thresholds between the 
various sub-labels. Thus, the ecotope-configuration file should look as follows, where customisable values are given as
`null`:
```json
{
  "salinity": {
    "variable": null,
    "fresh": null,
    "marine": null
  },
  "depth-1": {
    "low-water": null,
    "high-water": null
  },
  "hydrodynamics": {
    "stagnant": null,
    "sub-littoral": null,
    "littoral": null
  },
  "depth-2": {
    "sub-littoral": {
      "depth-deep": null,
      "depth-shallow": null,
      "low-water": null
    },
    "littoral": {
      "inundation-upper": null,
      "inundation-lower": null
    },
    "supra-littoral": {
      "frequency-1": null,
      "frequency-2": null,
      "frequency-3": null
    }
  },
  "substratum-2": {
    "soft": {
      "silt": null,
      "fines": null,
      "sand": null
    }
  }
}
```

**Note** that the tide-related key-words in the ecotope-configuration file (i.e., `depth-1 > low-water`, 
`depth-1 > high-water`, and `depth-2 > low-water`) consider the `z`-axis to be defined positive upwards. Thus, high 
water level is _**greater**_ than low water level.

**Note** that not all values are necessarily thresholds, e.g., `salinity > variable` is not a threshold but part of the
definition of whether the _Salinity_-label should be set to `V` (_Variable_). See the accompanying 
[publication]() for more details on the definitions in the ecotope-configuration file.

### Map-configuration file
Customisation of the map-configuration file requires the definition of less attributes. The map-configuration file 
should look as follows, where the customisable key-words are given as `null`:
```json
{
  "x-coordinates": null,
  "y-coordinates": null,
  "water-depth": null,
  "x-velocity": null,
  "y-velocity": null,
  "salinity": null,
  "depth-sign": null
}
```
**Note** that the `depth-sign` key-word reflects the sign used to describe the water depth in the output map-file, which 
may be different from the direction of the `z`-axis. `"depth-sign": "+"` means that the water depth is defined as a 
positive value when the bottom is _**below**_ the reference level (e.g. mean sea level); and vice versa. 

### Partial customisation
It is also possible to provide a partial configuration file. This would overwrite those key-words in the default 
configuration file (i.e., [`emma.json`](emma.json) or [`dfm4.json`](dfm4.json)) by the key-words defined in the partial,
custom configuration file. This is especially relevant for the ecotope-configuration file, as the map-configuration file
is fully dependent on the hydrodynamic model used between which there is generally no overlap in key-words.

An example of a partial customised ecotope-configuration file would look as follows (again with `null` representing
customised values):
```json
{
  "depth-1": {
    "low-water": null,
    "high-water": null
  }
}
```

This results in using [`emma.json`](emma.json) as the ecotope-configuration file in which the thresholds for `depth-1`
are customised.

It is also possible to customise only a single threshold:
```json
{
  "salinity": {
    "variable": null
  }
}
```
With the above partial configuration file, only the `variable` key-word is customised while the `fresh` and `marine`
key-words for `salinity` remain their default values (i.e., as in [`emma.json`](emma.json)).

**Note** that despite providing only a single element to be customised, the depth-level must comply with the original
configuration file, in this case the ecotope-configuration file.
