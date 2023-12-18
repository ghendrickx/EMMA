"""
Tests for `src/processing.py`.

Author: Gijs G. Hendrickx
"""
# pylint: disable=locally-disabled, missing-function-docstring, protected-access
import os

import numpy as np
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

    test = processing.__determine_ecotopes(nc_file)

    with open(csv_file, mode='r') as f:
        file = [line.rstrip().split(',') for line in f.readlines()]
    expected = tuple(zip(*file))

    for i, (x, y) in enumerate(zip(test, expected)):
        npt.assert_array_equal(x, np.array(y, dtype=(str if i == 2 else float)))


def test_map_ecotope():
    wd = __file__.split(os.sep)[:-2] + ['examples', 'ex_map_data']
    nc_file = os.sep.join(wd + ['output_map.nc'])
    csv_file = os.sep.join(wd + ['output.csv'])

    test = processing.map_ecotopes(nc_file, return_ecotopes='tuple', f_export=False)

    with open(csv_file, mode='r') as f:
        file = [line.rstrip().split(',') for line in f.readlines()]
    expected = tuple(zip(*file))

    for i, (x, y) in enumerate(zip(test, expected)):
        npt.assert_array_equal(x, np.array(y, dtype=(str if i == 2 else float)))
