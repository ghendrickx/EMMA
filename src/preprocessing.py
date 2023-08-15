"""
Pre-processing of output data of hydrodynamic model.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging
import os
import typing

import netCDF4
import numpy as np

_LOG = logging.getLogger(__name__)

CONFIG = dict()


class MapData:
    """Interface to open, read, and close a netCDF-file with built-in functions to extract the relevant data and
    compress any three-dimensional data to two-dimensional data (depth-averaged).
    """

    def __init__(self, file_name: str, wd: str = None) -> None:
        """
        :param file_name: netCDF file name with map-data
        :param wd: working directory, defaults to None

        :type file_name: str
        :type wd: str
        """
        self.file = os.path.join(wd or os.getcwd(), file_name)

        self._data = netCDF4.Dataset(self.file)
        self._velocity = None

        _LOG.info(f'Map-file loaded: {self.file}')

        if not CONFIG:
            _LOG.critical(f'No map-configuration defined when initialising {self.__class__.__name__}')

    @property
    def data(self) -> netCDF4.Dataset:
        """
        :return: netCDF dataset
        :rtype: netCDF4.Dataset
        """
        return self._data

    def close(self) -> None:
        """Close the netCDF dataset."""
        self._data.close()

        _LOG.info(f'NetCDF-file closed: {self.file}')

    def get_variable(self, variable: str, max_dim: int = 2) -> np.ndarray:
        """Retrieve a variable from the netCDF dataset based on the variable key-word.

        :param variable: variable key-word
        :param max_dim: maximum number of dimensions, defaults to 2

        :type variable: str
        :type max_dim: int

        :return: variable data
        :rtype: numpy.ndarray
        """
        # extract data
        data = self.data[variable][:]

        # reduce dimensions
        if len(data.shape) > max_dim:
            data = np.mean(data, axis=max_dim)

        # return data
        return data

    @property
    def _depth_sign(self) -> int:
        """Convert the sign of the water depth as written to the map-file by the hydrodynamic model to be positive
        downward---and vice versa.

        :return: sign of water depth
        :rtype: int
        """
        assert CONFIG['depth-sign'] in ('+', '-')
        return +1 if CONFIG['depth-sign'] == '+' else -1

    @property
    def x_coordinates(self) -> np.ndarray:
        """
        :return: x-coordinates
        :rtype: numpy.ndarray
        """
        return self.get_variable(CONFIG['x-coordinates'])

    @property
    def y_coordinates(self) -> np.ndarray:
        """
        :return: y-coordinates
        :rtype: numpy.ndarray
        """
        return self.get_variable(CONFIG['y-coordinates'])

    @property
    def water_depth(self) -> np.ndarray:
        """
        :return: water levels [m]
        :rtype: numpy.ndarray
        """
        return self._depth_sign * self.get_variable(CONFIG['water-depth'])

    @property
    def velocity(self) -> np.ndarray:
        """
        :return: depth-averaged flow velocity [m/s]
        :rtype: numpy.ndarray
        """
        if self._velocity is None:
            self._velocity = np.sqrt(
                self.get_variable(CONFIG['x-velocity']) ** 2 + self.get_variable(CONFIG['y-velocity']) ** 2
            )

        return self._velocity

    @property
    def salinity(self) -> np.ndarray:
        """
        :return: depth-averaged salinity [psu]
        :rtype: numpy.ndarray
        """
        return self.get_variable(CONFIG['salinity'])

    @property
    def grain_size(self) -> typing.Optional[np.ndarray]:
        """
        :return: grain-sizes [um]
        :rtype: numpy.ndarray
        """
        return None


def process_salinity(salinity: np.ndarray, time_axis: int = 0) -> typing.Tuple[np.ndarray, np.ndarray]:
    """Pre-process (depth-averaged) salinity time-series.

    :param salinity: (depth-averaged) salinity time-series
    :param time_axis: axis with temporal variability, defaults to 0

    :type salinity: numpy.ndarray
    :type time_axis: int, optional

    :return: temporal mean and standard deviation of (depth-averaged) salinity
    :rtype: tuple
    """
    # collapse time axis
    mean_salinity = np.ma.mean(salinity, axis=time_axis)
    std_salinity = np.ma.std(salinity, axis=time_axis)

    # logging
    _LOG.info('Salinity-data pre-processed')

    # return processed data
    return mean_salinity, std_salinity


def process_water_depth(
        water_depth: np.ndarray, time_axis: int = 0
) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pre-process water depth time-series.

    :param water_depth: water depth time-series
    :param time_axis: axis with temporal variability, defaults to 0

    :type water_depth: numpy.ndarray
    :type time_axis: int, optional

    :return: inundation duration and frequency
    :rtype: tuple
    """
    # collapse time axis
    mean_depth = np.ma.mean(water_depth, axis=time_axis)
    duration = np.ma.sum(water_depth > 0, axis=time_axis) / water_depth.shape[time_axis]
    sign_changes = np.ma.diff(np.sign(water_depth), axis=time_axis)
    frequency = np.count_nonzero(sign_changes, axis=time_axis) / 2

    # logging
    _LOG.info('Water depth- & flooding/drying-data pre-processed')

    # return processed data
    return mean_depth, duration, frequency


def process_velocity(velocity: np.ndarray, time_axis: int = 0) -> typing.Tuple[np.ndarray, np.ndarray]:
    """Pre-process flow velocity time-series.

    :param velocity: flow velocity time-series
    :param time_axis: axis with temporal variability, defaults to 0

    :type velocity: numpy.ndarray
    :type time_axis: int, optional

    :return: temporal median and maximum flow velocities
    :rtype: tuple
    """
    # collapse time axis
    median_velocity = np.ma.median(velocity, axis=time_axis)
    max_velocity = np.ma.max(velocity, axis=time_axis)

    # logging
    _LOG.info('Flow velocity-data pre-processed')

    # return processed data
    return median_velocity, max_velocity


def grain_size_estimation(
        median_velocity: np.ndarray, *,
        shields: float = .07, chezy: float = 50, r_density: float = 1.58, c_friction: float = None
) -> np.ndarray:
    """Estimation of grain sizes based on (median) flow velocities. The grain sizes can either be determined from the
    critical Shields parameter, the Chezy coefficient, and the relative density; or a variable encompassing all three
    variables, representing a friction value (`c_friction`). Note that `c_friction` is inversely related to the product
    of the other three variables.

    :param median_velocity: temporal median flow velocities
    :param shields: critical Shields parameters [-], defaults to .03
    :param chezy: Chezy coefficient [m^(1/2) /s], defaults to 60
    :param r_density: relative density between sediment and water [-], defaults to 1.58
    :param c_friction: proxy of bottom friction coefficient [s2 /m], defaults to None

    :type median_velocity: numpy.ndarray
    :type shields: float, optional
    :type chezy: float, optional
    :type r_density: float, optional
    :type c_friction: float, optional

    :return: grain sizes [um]
    :rtype: numpy.ndarray
    """
    if c_friction is None:
        c_friction = 1e6 / (shields * r_density * chezy ** 2)
    return c_friction * median_velocity ** 2
