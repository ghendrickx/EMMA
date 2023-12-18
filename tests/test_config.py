"""
Tests for `config/config_file.py`.

Author: Gijs G. Hendrickx
"""
import functools

import pytest

from config import config_file as cf

# setting configuration
ECO_DEF_CONFIG = cf.load_config('emma.json')
ECO_INT_CONFIG = cf.load_config('emma.json', 'zes1.json')
ECO_CUS_CONFIG = cf.load_config('emma.json', {
    'salinity': {'marine': 20},
    'hydrodynamics': {'stagnant': .1},
    'depth-2': {
        'supra-littoral': {
            'frequency-3': 10,
            'frequency-4': 0  # non-existing configuration keyword should be accepted (and skipped)
        }
    }
})

MAP_DEF_CONFIG = cf.load_config('dfm1.json')
MAP_INT_CONFIG = cf.load_config('dfm1.json', 'dfm4.json')
MAP_CUS_CONFIG = cf.load_config('dfm1.json', {
    'depth-sign': '-'
})

# helper function


def eco_keys(d_config):
    return [
        (d_config, ('salinity', 'depth-1', 'hydrodynamics', 'depth-2', 'substratum-2')),
        (d_config['salinity'], ('variable', 'fresh', 'marine')),
        (d_config['depth-1'], ('low-water', 'high-water')),
        (d_config['hydrodynamics'], ('stagnant', 'sub-littoral', 'littoral')),
        (d_config['depth-2'], ('sub-littoral', 'littoral', 'supra-littoral')),
        (d_config['substratum-2'], ('soft',)),
        (d_config['depth-2']['sub-littoral'], ('depth-deep', 'depth-shallow')),
        (d_config['depth-2']['littoral'], ('inundation-upper', 'inundation-lower')),
        (d_config['depth-2']['supra-littoral'], ('frequency-1', 'frequency-2', 'frequency-3')),
    ]


def map_keys():
    return 'x-coordinates', 'y-coordinates', 'water-depth', 'x-velocity', 'y-velocity', 'salinity', 'depth-sign'


# tests: ecotope-configuration


@pytest.mark.parametrize(
    'dictionary, expected',
    eco_keys(ECO_DEF_CONFIG) + eco_keys(ECO_INT_CONFIG) + eco_keys(ECO_CUS_CONFIG)
)
def test_eco_keys(dictionary, expected):
    assert all(k in dictionary for k in expected)


@pytest.mark.parametrize(
    'keys, value',
    [
        (('salinity', 'variable'), 4),
        (('salinity', 'fresh'), 5.4),
        (('salinity', 'marine'), 18),
        (('depth-1', 'low-water'), -2.31),
        (('depth-1', 'high-water'), 1.85),
        (('hydrodynamics', 'stagnant'), 0),
        (('hydrodynamics', 'sub-littoral'), .7),
        (('hydrodynamics', 'littoral'), .7),
        (('depth-2', 'sub-littoral', 'depth-deep'), 30),
        (('depth-2', 'sub-littoral', 'depth-shallow'), 10),
        (('depth-2', 'littoral', 'inundation-upper'), .75),
        (('depth-2', 'littoral', 'inundation-lower'), .25),
        (('depth-2', 'supra-littoral', 'frequency-1'), 300),
        (('depth-2', 'supra-littoral', 'frequency-2'), 150),
        (('depth-2', 'supra-littoral', 'frequency-3'), 50),
        (('substratum-2', 'soft', 'silt'), 25),
        (('substratum-2', 'soft', 'fines'), 250),
        (('substratum-2', 'soft', 'sand'), 2000),
    ]
)
def test_default_eco_config(keys, value):
    val = functools.reduce(lambda d, k: d.get(k), keys, ECO_DEF_CONFIG)
    assert val == value


@pytest.mark.parametrize(
    'keys, value',
    [
        (('salinity', 'variable'), 4),
        (('salinity', 'fresh'), 5.4),
        (('salinity', 'marine'), 18),
        (('depth-1', 'low-water'), -2.31),
        (('depth-1', 'high-water'), 1.85),
        (('hydrodynamics', 'stagnant'), 0),
        (('hydrodynamics', 'sub-littoral'), .8),
        (('hydrodynamics', 'littoral'), .2),
        (('depth-2', 'sub-littoral', 'depth-deep'), 10),
        (('depth-2', 'sub-littoral', 'depth-shallow'), 5),
        (('depth-2', 'littoral', 'inundation-upper'), .75),
        (('depth-2', 'littoral', 'inundation-lower'), .25),
        (('depth-2', 'supra-littoral', 'frequency-1'), 300),
        (('depth-2', 'supra-littoral', 'frequency-2'), 150),
        (('depth-2', 'supra-littoral', 'frequency-3'), 50),
        (('substratum-2', 'soft', 'silt'), 25),
        (('substratum-2', 'soft', 'fines'), 250),
        (('substratum-2', 'soft', 'sand'), 2000),
    ]
)
def test_builtin_eco_config(keys, value):
    val = functools.reduce(lambda d, k: d.get(k), keys, ECO_INT_CONFIG)
    assert val == value


@pytest.mark.parametrize(
    'keys, value',
    [
        (('salinity', 'variable'), 4),
        (('salinity', 'fresh'), 5.4),
        (('salinity', 'marine'), 20),
        (('depth-1', 'low-water'), -2.31),
        (('depth-1', 'high-water'), 1.85),
        (('hydrodynamics', 'stagnant'), .1),
        (('hydrodynamics', 'sub-littoral'), .7),
        (('hydrodynamics', 'littoral'), .7),
        (('depth-2', 'sub-littoral', 'depth-deep'), 30),
        (('depth-2', 'sub-littoral', 'depth-shallow'), 10),
        (('depth-2', 'littoral', 'inundation-upper'), .75),
        (('depth-2', 'littoral', 'inundation-lower'), .25),
        (('depth-2', 'supra-littoral', 'frequency-1'), 300),
        (('depth-2', 'supra-littoral', 'frequency-2'), 150),
        (('depth-2', 'supra-littoral', 'frequency-3'), 10),
        (('substratum-2', 'soft', 'silt'), 25),
        (('substratum-2', 'soft', 'fines'), 250),
        (('substratum-2', 'soft', 'sand'), 2000),
    ]
)
def test_custom_eco_config(keys, value):
    val = functools.reduce(lambda d, k: d.get(k), keys, ECO_CUS_CONFIG)
    assert val == value


# tests: map-configuration


@pytest.mark.parametrize(
    'dictionary, expected',
    [
        (MAP_DEF_CONFIG, map_keys()),
        (MAP_INT_CONFIG, map_keys()),
        (MAP_CUS_CONFIG, map_keys()),
    ]
)
def test_map_keys(dictionary, expected):
    assert all(k in dictionary for k in expected)


@pytest.mark.parametrize(
    'key, value',
    [
        ('x-coordinates', 'FlowElem_xcc'),
        ('y-coordinates', 'FlowElem_ycc'),
        ('water-depth', 'waterdepth'),
        ('x-velocity', 'ucx'),
        ('y-velocity', 'ucy'),
        ('salinity', 'sa1'),
        ('depth-sign', '+'),
    ]
)
def test_default_map_config(key, value):
    assert MAP_DEF_CONFIG[key] == value


@pytest.mark.parametrize(
    'key, value',
    [
        ('x-coordinates', 'mesh2d_face_x'),
        ('y-coordinates', 'mesh2d_face_y'),
        ('water-depth', 'mesh2d_waterdepth'),
        ('x-velocity', 'mesh2d_ucx'),
        ('y-velocity', 'mesh2d_ucy'),
        ('salinity', 'mesh2d_sa1'),
        ('depth-sign', '+'),
    ]
)
def test_builtin_map_config(key, value):
    assert MAP_INT_CONFIG[key] == value


@pytest.mark.parametrize(
    'key, value',
    [
        ('x-coordinates', 'FlowElem_xcc'),
        ('y-coordinates', 'FlowElem_ycc'),
        ('water-depth', 'waterdepth'),
        ('x-velocity', 'ucx'),
        ('y-velocity', 'ucy'),
        ('salinity', 'sa1'),
        ('depth-sign', '-'),
    ]
)
def test_custom_map_config(key, value):
    assert MAP_CUS_CONFIG[key] == value


# tests: failing configuration


@pytest.mark.parametrize(
    'user, error',
    [
        ('non-existing-config-file.json', FileNotFoundError),
        (['dict', 'as', 'list'], TypeError),
    ]
)
def test_config_errors(user, error):
    with pytest.raises(error):
        cf.load_config('emma.json', user)


# tests: nested dictionary


@pytest.mark.parametrize(
    'dict1, dict2, expected',
    [
        ({'key1': 0}, {'key1': 1}, {'key1': 1}),
        ({'key1': {'s1': 0, 's2': 0}}, {'key1': {'s1': 1}}, {'key1': {'s1': 1, 's2': 0}}),
        ({'key1': {'s1': 0, 's2': 0}, 'key2': 0}, {'key1': {'s1': 1}}, {'key1': {'s1': 1, 's2': 0}, 'key2': 0}),
        ({'key1': {'s1': 0, 's2': 0}}, {'key1': {'s1': 1, 's3': 1}}, {'key1': {'s1': 1, 's2': 0}}),
    ]
)
def test_nested_dict_update(dict1, dict2, expected):
    d = cf._update_nested_dict(dict1, dict2)
    assert d == expected
