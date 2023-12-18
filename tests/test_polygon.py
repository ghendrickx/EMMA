"""
Tests for `src/performance.py`, polygon and grid handling functions.

Author: Gijs G. Hendrickx
"""
import pytest
from shapely.geometry import Point

from src import performance as pf


@pytest.fixture
def dummy_feature():
    """Create a representative feature for testing."""
    return dict(
        geometry=dict(
            coordinates=[[
                [0, 0],
                [0, 5],
                [5, 5],
                [5, 0]
            ]]
        ),
        properties=dict(
            zes_code='Z2.222f'
        )
    )


@pytest.mark.parametrize(
    'points, length',
    [
        ([Point(2, 2)], 1),
        ([Point(7, 7)], 0),
        ([Point(1, 1), Point(2, 2), Point(3, 3)], 3),
        ([Point(2, 2), Point(7, 7)], 1)
    ]
)
def test_point_in_feature(dummy_feature, points, length):
    out = pf.points_in_feature(dummy_feature, points)
    assert len(out) == length


def test_assign_zes_code(dummy_feature):
    out = pf.points_in_feature(dummy_feature, [Point(1, 1), Point(2, 2), Point(3, 3)])
    assert all(v == 'Z2.222f' for v in out.values())


@pytest.mark.parametrize(
    'point, length',
    [
        ([Point(2, 2)], 1),
        ([Point(7, 7)], 0)
    ]
)
def test_quick_check(dummy_feature, point, length):
    out = pf.points_in_feature(dummy_feature, point, quick_check=True)
    assert len(out) == length
