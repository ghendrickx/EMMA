"""
Tests for `src/processing.py`.

Author: Gijs G. Hendrickx
"""
import pytest

from src import processing


def equal_dict(test: dict, expected: dict):
    assert all(k in expected for k in test)
    assert all(k in test for k in expected)
    assert all(expected[k] == v for k, v in test.items())
    assert all(test[k] == v for k, v in expected.items())


@pytest.mark.parametrize(
    'x, y, labels, expected',
    [
        ([0, 0], [0, 1], ['c', 'c'], {
            (0, 0): 'c',
            (0, 1): 'c'
        }),
        ([0, 0], [0, 0], ['c', 'c'], {
            (0, 0): 'c',
        }),
        ([0, 0], [0, 1], ['c', 'z'], {
            (0, 0): 'c',
            (0, 1): 'z'
        })
    ]
)
def test_convert2dict(x, y, labels, expected):
    out = processing.convert2dict(x, y, labels)
    equal_dict(out, expected)
