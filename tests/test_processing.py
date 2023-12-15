"""
Tests for `src/processing.py`.

Author: Gijs G. Hendrickx
"""
import os

import numpy.testing as npt
import pytest

from src import processing


@pytest.mark.parametrize(
    'data, expected',
    [
        (([0], [0], ['c']), {
            (0, 0): 'c',
        }),
        (([0, 0], [0, 1], ['c', 'c']), {
            (0, 0): 'c',
            (0, 1): 'c',
        }),
        (([0, 0], [0, 0], ['c', 'c']), {
            (0, 0): 'c',
        }),
        (([0, 0], [0, 1], ['c1', 'c2']), {
            (0, 0): 'c1',
            (0, 1): 'c2',
        })
    ]
)
def test_convert2dict(data, expected):
    out = processing.convert2dict(*data)
    assert out == expected


@pytest.mark.parametrize(
    'data, expected',
    [
        ({(0, 0): 'c'}, ([0], [0], ['c'])),
        ({
            (0, 0): 'c',
            (0, 1): 'c',
        }, ([0, 0], [0, 1], ['c', 'c'])),
        ({
            (0, 0): 'c1',
            (0, 1): 'c2',
        }, ([0, 0], [0, 1], ['c1', 'c2'])),
    ]
)
def test_convert2tuple(data, expected):
    out = processing.convert2tuple(data)
    for x, y in zip(out, expected):
        npt.assert_array_equal(x, y)


def test_determine_ecotopes():
    wd = __file__.split(os.sep)[:-2] + ['examples', 'ex_map_data']
    nc_file = os.sep.join(wd + ['output_map.nc'])
    csv_file = os.sep.join(wd + ['output.csv'])

    test = processing.__determine_ecotopes(nc_file, f_map_config='dfm1.json')

    with open(csv_file, mode='r') as f:
        file = [line.rstrip().split(',') for line in f.readlines()]
    expected = tuple(zip(*file))

    for x, y in zip(test, expected):
        npt.assert_array_equal(x, y)
