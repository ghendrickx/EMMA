"""
Tests for `src/preprocessing.py`.

Author: Gijs G. Hendrickx
"""
import pytest

import numpy as np
from shapely.geometry import Point

from config import config_file
from src import preprocessing as pre

"""Set configuration file"""
pre.glob.MODEL_CONFIG = config_file.load_config('dfm1.json')

"""pytest.fixtures"""


@pytest.fixture
def dummy_time_series():
    """Create a random array to test the order of its statistics."""
    return np.random.random((100, 100))


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


"""TestsClasses"""


class TestProcessTimeSeries:
    """Tests for `process_salinity()` (prefix: `test_salinity`), `process_water_depth()` (prefix: `test_water_depth`),
    `process_velocity()` (prefix: `test_velocity`), and `grain_size_estimation()` (`test_grain_size_estimation()`).
    """

    def test_salinity(self, dummy_time_series):
        """Processing of salinity time-series should return a tuple with the temporal minimum, mean, and maximum values,
        processed over the time-axis (default: 0).
        """
        ts = dummy_time_series
        truth = np.mean(ts, axis=0), np.std(ts, axis=0)
        output = pre.process_salinity(ts)
        assert np.array_equal(truth, output)

    def test_salinity_time_axis(self, dummy_time_series):
        """Processing of salinity time-series should return a tuple with the temporal minimum, mean, and maximum values,
        processed over the time-axis, here set to 1.
        """
        ts = dummy_time_series
        truth = np.mean(ts, axis=1), np.std(ts, axis=1)
        output = pre.process_salinity(ts, time_axis=1)
        assert np.array_equal(truth, output)

    def test_water_depth(self, dummy_time_series):
        """Processing of water depth time-series should return a tuple with the temporal mean water depth, flood
        duration, and flood frequency. The flood duration and frequency cannot be tested reasonably.
        """
        ts = dummy_time_series
        truth = np.mean(ts, axis=0)
        output = pre.process_water_depth(ts)
        assert len(output) == 3
        assert np.array_equal(truth, output[0])

    def test_velocity(self, dummy_time_series):
        """Processing of flow velocity time-series should return a tuple with the temporal median and maximum values,
        processed over the time-axis (default: 0).
        """
        ts = dummy_time_series
        truth = np.median(ts, axis=0), np.max(ts, axis=0)
        output = pre.process_velocity(ts)
        assert np.array_equal(truth, output)

    def test_grain_size_estimation(self):
        """Estimation of grain sizes based on the median flow velocity with default values of the optional arguments:
        critical Shields parameter (`shields=.07`), Chezy coefficient (`chezy=50`), and relative density
        (`r_density=1.58`).
        """
        truth = np.array([0, 3616.6365280289324])
        output = pre.grain_size_estimation(np.array([0, 1]), shields=.07, chezy=50, r_density=1.58)
        for t, o in zip(truth, output):
            assert pytest.approx(t) == o

    def test_grain_size_estimation_custom(self):
        """Estimation of grain sizes based on the median flow velocity with custom values of the optional arguments:
        critical Shields parameter (`shields=.07`), Chezy coefficient (`chezy=50`), and relative density
        (`r_density=1.58`).
        """
        truth = np.array([0, 5860.29067042])
        output = pre.grain_size_estimation(np.array([0, 1]), shields=.03, chezy=60, r_density=1.58)
        for t, o in zip(truth, output):
            assert pytest.approx(t) == o

    def test_grain_size_estimation_mod(self):
        """Estimation of grain sizes based on the median flow velocity with EMMA's calibrated, grouped friction
        parameter (`c_friction=1300`).
        """
        truth = np.array([0, 1300])
        output = pre.grain_size_estimation(np.array([0, 1]), c_friction=1300)
        for t, o in zip(truth, output):
            assert pytest.approx(t) == o


class TestPointsInFeature:
    """Tests for `points_in_feature()`."""

    def test_single_point_inside(self, dummy_feature):
        out = pre.points_in_feature(dummy_feature, [Point(2, 2)])
        assert len(out) == 1

    def test_single_point_outside(self, dummy_feature):
        out = pre.points_in_feature(dummy_feature, [Point(7, 7)])
        assert len(out) == 0

    def test_multi_point_inside(self, dummy_feature):
        out = pre.points_in_feature(dummy_feature, [Point(1, 1), Point(2, 2), Point(3, 3)])
        assert len(out) == 3

    def test_multi_point_mixed(self, dummy_feature):
        out = pre.points_in_feature(dummy_feature, [Point(2, 2), Point(7, 7)])
        assert len(out) == 1

    def test_assign_zes_code(self, dummy_feature):
        out = pre.points_in_feature(dummy_feature, [Point(1, 1), Point(2, 2), Point(3, 3)])
        assert all(v == 'Z2.222f' for v in out.values())

    def test_quick_check_outside(self, dummy_feature):
        out = pre.points_in_feature(dummy_feature, [Point(7, 7)], quick_check=True)
        assert len(out) == 0

    def test_quick_check_inside(self, dummy_feature):
        out = pre.points_in_feature(dummy_feature, [Point(2, 2)], quick_check=True)
        assert len(out) == 1
