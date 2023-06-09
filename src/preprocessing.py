"""
Pre-processing of output data of hydrodynamic model.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import os

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
