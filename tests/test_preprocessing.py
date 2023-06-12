"""
Tests for `preprocessing.py`.

Author: Gijs G. Hendrickx
"""
import pytest

import numpy as np

from src import preprocessing as pre

"""pytest.fixtures"""


@pytest.fixture
def dummy_time_series():
    return np.random.random((100, 100))


"""TestsClasses"""


class TestProcessTimeSeries:

    def test_salinity(self, dummy_time_series):
        """Processing of salinity time-series should return a tuple with the temporal minimum, mean, and maximum values,
        processed over the time-axis (default: 0).
        """
        ts = dummy_time_series
        truth = np.min(ts, axis=0), np.mean(ts, axis=0), np.max(ts, axis=0)
        output = pre.process_salinity(ts)
        assert np.array_equal(truth, output)

    def test_salinity_time_axis(self, dummy_time_series):
        """Processing of salinity time-series should return a tuple with the temporal minimum, mean, and maximum values,
        processed over the time-axis, here set to 1.
        """
        ts = dummy_time_series
        truth = np.min(ts, axis=1), np.mean(ts, axis=1), np.max(ts, axis=1)
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
        critical Shields parameter (`shields=.03`), Chezy coefficient (`chezy=60`), and relative density
        (`r_density=1.58`).
        """
        truth = np.array([0, 5860.29067042])
        output = pre.grain_size_estimation(np.array([0, 1]))
        for t, o in zip(truth, output):
            assert pytest.approx(t) == o
