"""
Pre-processing of output data of hydrodynamic model.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import os
from typing import Tuple

import netCDF4
import numpy as np


class MapData:

    def __init__(self, file_name: str, wd: str=None) -> None:
        """
        :param file_name: netCDF file name with map-data
        :param wd: working directory, defaults to None

        :type file_name: str
        :type wd: str
        """
        self.file_name = file_name
        self.wd = wd or os.getcwd()

        self._data = netCDF4.Dataset(os.path.join(self.wd, self.file_name))
        self._velocity = None

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

    def get_variable(self, variable: str, max_dim: int=2) -> np.ndarray:
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
    def x_coordinates(self) -> np.ndarray:
        """
        :return: x-coordinates
        :rtype: numpy.ndarray
        """
        return self.get_variable('FlowElem_xcc')

    @property
    def y_coordinates(self) -> np.ndarray:
        """
        :return: y-coordinates
        :rtype: numpy.ndarray
        """
        return self.get_variable('FlowElem_ycc')

    @property
    def water_depth(self) -> np.ndarray:
        """
        :return: water levels [m]
        :rtype: numpy.ndarray
        """
        return self.get_variable('waterdepth')

    @property
    def velocity(self) -> np.ndarray:
        """
        :return: depth-averaged flow velocity [m/s]
        :rtype: numpy.ndarray
        """
        if self._velocity is None:
            self._velocity = np.sqrt(self.get_variable('ucx') ** 2 + self.get_variable('ucy') ** 2)

        return self._velocity

    @property
    def salinity(self) -> np.ndarray:
        """
        :return: depth-averaged salinity [psu]
        :rtype: numpy.ndarray
        """
        return self.get_variable('salinity')


def process_salinity(salinity: np.ndarray, time_axis: int=0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pre-process (depth-averaged) salinity time-series.

    :param salinity: (depth-averaged) salinity time-series
    :param time_axis: axis with temporal variability, defaults to 0

    :type salinity: numpy.ndarray
    :type time_axis: int, optional

    :return: temporal minimum, mean, and maximum (depth-averaged) salinity
    :rtype: tuple
    """
    # collapse time axis
    min_salinity = np.min(salinity, axis=time_axis)
    mean_salinity = np.mean(salinity, axis=time_axis)
    max_salinity = np.max(salinity, axis=time_axis)

    # return processed data
    return min_salinity, mean_salinity, max_salinity


def process_inundation(water_depth: np.ndarray, time_axis: int=0) -> np.ndarray:
    """Pre-process inundation time-series.

    :param water_depth: water depth time-series
    :param time_axis: axis with temporal variability, defaults to 0

    :type water_depth: numpy.ndarray
    :type time_axis: int, optional

    :return: inundation percentages
    :rtype: numpy.ndarray
    """
    # collapse time axis
    inundation = np.sum(water_depth > 0, axis=time_axis) / water_depth.shape[time_axis]

    # return processed data
    return inundation


def process_frequency(water_depth: np.ndarray, time_axis: int=0) -> np.ndarray:
    """Pre-process inundation frequency time-series.

    :param water_depth: water depth time-series
    :param time_axis: axis with temporal variability, defaults to 0

    :type water_depth: numpy.ndarray
    :type time_axis: int, optional

    :return: inundation frequencies
    :rtype: numpy.ndarray
    """
    # collapse time axis
    sign_changes = np.diff(np.sign(water_depth), axis=time_axis)
    frequency = np.count_nonzero(sign_changes, axis=time_axis) / 2

    # return processed data
    return frequency
