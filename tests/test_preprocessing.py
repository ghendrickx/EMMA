"""
Tests for `src/preprocessing.py`.

Author: Gijs G. Hendrickx
"""
# pylint: disable=locally-disabled, missing-function-docstring, protected-access
import pytest

import numpy as np
import numpy.testing as npt

from config import config_file
from src import preprocessing as pre

# setting configuration
pre.glob.MODEL_CONFIG = config_file.load_config('dfm1.json')

# dummy time-series
TIME_SERIES = np.random.random((100, 100))


# tests


class TestProcessTimeSeries:
    """Tests for `process_salinity()` (prefix: `test_salinity`), `process_water_depth()` (prefix: `test_water_depth`),
    `process_velocity()` (prefix: `test_velocity`), and `grain_size_estimation()` (`test_grain_size_estimation()`).
    """

    def test_salinity(self):
        """Processing of salinity time-series should return a tuple with the temporal minimum, mean, and maximum values,
        processed over the time-axis (default: 0).
        """
        truth = np.mean(TIME_SERIES, axis=0), np.std(TIME_SERIES, axis=0)
        output = pre.process_salinity(TIME_SERIES)
        assert np.array_equal(truth, output)

    def test_salinity_time_axis(self):
        """Processing of salinity time-series should return a tuple with the temporal minimum, mean, and maximum values,
        processed over the time-axis, here set to 1.
        """
        truth = np.mean(TIME_SERIES, axis=1), np.std(TIME_SERIES, axis=1)
        output = pre.process_salinity(TIME_SERIES, time_axis=1)
        assert np.array_equal(truth, output)

    def test_water_depth(self):
        """Processing of water depth time-series should return a tuple with the temporal mean water depth, flood
        duration, and flood frequency. The flood duration and frequency cannot be tested reasonably.
        """
        truth = np.mean(TIME_SERIES, axis=0)
        output = pre.process_water_depth(TIME_SERIES)
        assert len(output) == 3
        assert np.array_equal(truth, output[0])

    def test_velocity(self):
        """Processing of flow velocity time-series should return a tuple with the temporal median and maximum values,
        processed over the time-axis (default: 0).
        """
        truth = np.median(TIME_SERIES, axis=0), np.max(TIME_SERIES, axis=0)
        output = pre.process_velocity(TIME_SERIES)
        assert np.array_equal(truth, output)


@pytest.mark.parametrize(
    'shields, chezy, r_density, c_friction, expected',
    [
        (.07, 50, 1.58, None, [0, 3616.6365280289324]),
        (.03, 60, 1.58, None, [0, 5860.29067042]),
        (None, None, None, 1300, [0, 1300])
    ]
)
def test_grain_size_estimation(shields, chezy, r_density, c_friction, expected):
    out = pre.grain_size_estimation(
        np.array([0, 1]), shields=shields, chezy=chezy, r_density=r_density, c_friction=c_friction
    )
    npt.assert_array_almost_equal(out, expected)
