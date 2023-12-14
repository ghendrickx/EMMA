"""
Tests for `src/processing.py`.

Author: Gijs G. Hendrickx
"""
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
        ([0, 0], [0, 1], ['c', 'z'], {
            (0, 0): 'c',
            (0, 1): 'z',
        })
    ]
)
def test_convert2dict(x, y, labels, expected):
    out = processing.convert2dict(x, y, labels)
    assert out == expected
