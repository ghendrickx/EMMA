"""
Pre-processing of output data of hydrodynamic model.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging
import os
import typing

import numpy as np
import xarray as xr

from src import _globals as glob

_LOG = logging.getLogger(__name__)


class MapData:
    """Interface to open, read, and close a netCDF-file with built-in functions to extract the relevant data and
    compress any three-dimensional data to two-dimensional data (depth-averaged).
    """

    def __init__(self, file_name: str, wd: str = None, **kwargs) -> None:
        """
        :param file_name: netCDF file name with map-data
        :param wd: working directory, defaults to None

        :type file_name: str
        :type wd: str
        """
        self.file = os.path.join(wd or os.getcwd(), file_name)

        self._data = xr.open_dataset(self.file)
        self._velocity = None

        _LOG.info(f'Map-file loaded: {self.file}')

        if not glob.MODEL_CONFIG:
            _LOG.critical(f'No map-configuration defined when initialising {self.__class__.__name__}')

        self._map_format: str = kwargs.get('map_format')

    def __enter__(self) -> 'MapData':
        """Open context manager.

        :return: dataset
        :rtype: src.preprocessing.MapData
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit (i.e., close) context manager."""
        self.close()

    def __getitem__(self, item: str) -> np.ndarray:
        """Get item (i.e., variable data) from dataset.

        First, check if the item is an attribute of the object, i.e., defined as quick-access variable; second, use the
        `.get_variable()`-method to get the variable's data.

        :param item: variable name
        :type item: str

        :return: variable data
        :rtype: numpy.ndarray
        """
        # as quick-access defined
        if hasattr(self, item):
            return getattr(self, item)

        # not as quick-access defined
        return self.get_variable(item)

    @property
    def data(self) -> xr.Dataset:
        """
        :return: netCDF dataset
        :rtype: xarray.Dataset
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
        data = self.data[variable].to_masked_array()

        # reduce dimensions
        if len(data.shape) > max_dim:
            data = np.mean(data, axis=max_dim)

        # partition handler
        if self._map_format in ('dfm1', 'dfm4'):
            data = self.partition_handler(data)
        elif self._map_format is not None:
            _LOG.warning(f'Unknown map-format ({self._map_format}) skipped; this may influence the results.')

        # return data
        return data

    @property
    def _depth_sign(self) -> int:
        """Convert the sign of the water depth as written to the map-file by the hydrodynamic model to be positive
        downward---and vice versa.

        :return: sign of water depth
        :rtype: int
        """
        assert glob.MODEL_CONFIG['depth-sign'] in ('+', '-')
        return +1 if glob.MODEL_CONFIG['depth-sign'] == '+' else -1

    @property
    def x_coordinates(self) -> np.ndarray:
        """
        :return: x-coordinates
        :rtype: numpy.ndarray
        """
        return self.get_variable(glob.MODEL_CONFIG['x-coordinates'])

    @property
    def y_coordinates(self) -> np.ndarray:
        """
        :return: y-coordinates
        :rtype: numpy.ndarray
        """
        return self.get_variable(glob.MODEL_CONFIG['y-coordinates'])

    @property
    def water_depth(self) -> np.ndarray:
        """
        :return: water levels [m]
        :rtype: numpy.ndarray
        """
        return self._depth_sign * self.get_variable(glob.MODEL_CONFIG['water-depth'])

    @property
    def velocity(self) -> np.ndarray:
        """
        :return: depth-averaged flow velocity [m/s]
        :rtype: numpy.ndarray
        """
        if self._velocity is None:
            self._velocity = np.sqrt(
                self.get_variable(glob.MODEL_CONFIG['x-velocity']) ** 2 +
                self.get_variable(glob.MODEL_CONFIG['y-velocity']) ** 2
            )

        return self._velocity

    @property
    def salinity(self) -> np.ndarray:
        """
        :return: depth-averaged salinity [psu]
        :rtype: numpy.ndarray
        """
        return self.get_variable(glob.MODEL_CONFIG['salinity'])

    @property
    def grain_size(self) -> typing.Optional[np.ndarray]:
        """
        :return: grain-sizes [um]
        :rtype: numpy.ndarray
        """
        return None

    """partition handler"""

    @property
    def i_domain(self) -> typing.Union[np.ndarray, None]:
        """Domain number present in DFM map-output, which labels the grid cells to the partitioning domain of which the
        map-output is the result. Domain numbers from other partitions must be considered as ghost cells, required for
        computational reasons.

        :return: domain numbers
        :rtype: numpy.ndarray, None

        :raise NotImplementedError: if `map_format` is unknown
        """
        if self._map_format is None:
            return
        elif self._map_format == 'dfm1':
            return self.data['FlowElemDomain'].to_masked_array()
        elif self._map_format == 'dfm4':
            return self.data['mesh2d_flowelem_domain'].to_masked_array()
        raise NotImplementedError(f'No implementation for `map_format={self._map_format}`')

    @property
    def i_partition(self) -> typing.Union[int, None]:
        """Domain number of the considered partition, i.e., the partition number.

        :return: partition number
        :rtype: int, None
        """
        i = str(self.file.split('_')[-2])
        if i.isnumeric():
            return int(i)

    def partition_handler(self, data: np.ndarray) -> np.ndarray:
        """Process data to remove ghost cells present as a result

        :param data:
        :return:
        """
        if self.i_partition is not None:
            i_not_ghost = np.flatnonzero(self.i_domain == self.i_partition)
            return data.take(i_not_ghost, axis=(len(data.shape) - 1))

        return data


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
