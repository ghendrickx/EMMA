"""
Tests for `src/processing.py`.

Author: Gijs G. Hendrickx
"""
import numpy.testing as npt
import pytest

from src import processing


@pytest.mark.parametrize(
    'x, y, labels, expected',
    [
        ([0], [0], ['c'], {
            (0, 0): 'c',
        }),
        ([0, 0], [0, 1], ['c', 'c'], {
            (0, 0): 'c',
            (0, 1): 'c',
        }),
        ([0, 0], [0, 0], ['c', 'c'], {
            (0, 0): 'c',
        }),
        ([0, 0], [0, 1], ['c1', 'c2'], {
            (0, 0): 'c1',
            (0, 1): 'c2',
        })
    ]
)
def test_convert2dict(x, y, labels, expected):
    out = processing.convert2dict(x, y, labels)
    assert out == expected


@pytest.mark.parametrize(
    'xy_labels, expected',
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
def test_convert2tuple(xy_labels, expected):
    out = processing.convert2tuple(xy_labels)
    for x, y in zip(out, expected):
        npt.assert_array_equal(x, y)
