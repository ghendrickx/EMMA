"""
Tests for `config/config_file.py`.

Author: Gijs G. Hendrickx
"""
import pytest

from config.config_file import load_config

TEST_CONFIG = load_config('emma.json')


@pytest.mark.parametrize(
    'dictionary, expected',
    [
        (TEST_CONFIG, ('salinity', 'depth-1', 'hydrodynamics', 'depth-2', 'substratum-2')),
        (TEST_CONFIG['salinity'], ('variable', 'fresh', 'marine')),
        (TEST_CONFIG['depth-1'], ('low-water', 'high-water')),
        (TEST_CONFIG['hydrodynamics'], ('stagnant', 'sub-littoral', 'littoral')),
        (TEST_CONFIG['depth-2'], ('sub-littoral', 'littoral', 'supra-littoral')),
        (TEST_CONFIG['substratum-2'], ('soft',)),
        (TEST_CONFIG['depth-2']['sub-littoral'], ('depth-deep', 'depth-shallow')),
        (TEST_CONFIG['depth-2']['littoral'], ('inundation-upper', 'inundation-lower')),
        (TEST_CONFIG['depth-2']['supra-littoral'], ('frequency-1', 'frequency-2', 'frequency-3')),
    ]
)
def test_keys(dictionary, expected):
    keys = list(dictionary.keys())
    assert all(k in keys for k in expected)
