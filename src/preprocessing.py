"""
Pre-processing of output data of hydrodynamic model.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import functools
import json
import logging
import multiprocessing as mp
import os
import typing

import netCDF4
import numpy as np
from shapely import geometry

from src._globals import CONFIG, _TypeXYLabel

_LOG = logging.getLogger(__name__)


"""Pre-processing of hydrodynamic model data"""


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


"""Pre-processing of polygon-data"""


def csv2grid(file: str) -> _TypeXYLabel:
    """Transform *.csv-file with (x, y, label)-data to {(x, y): label}-formatted data.

    :param file: *.csv-file
    :type file: str

    :return: spatial distribution of ecotope-labels
    :rtype: dict[tuple[float, float], str]
    """
    # read file
    with open(file, mode='r') as f:
        data = [line.rstrip().split(',') for line in f.readlines()]

    # check file content
    if not len(data[0]) == 3:
        msg = f'CSV-file must contain three (3) columns (x, y, label); {len(data[0])} given'
        raise ValueError(msg)

    # transform data
    result = {(p[0], p[1]): p[2] for p in data}

    # return transformed data
    return result


def points_in_feature(feature: dict, points: typing.Collection[geometry.Point], **kwargs) -> dict:
    # optional arguments
    quick_check: bool = kwargs.get('quick_check_grid_in_polygon', False)
    grid: dict = kwargs.get('grid')
    assert quick_check == bool(grid), \
        f'Both or neither `quick_check` and/nor `grid` should be `True`: ' \
        f'`quick_check={quick_check}` and `bool(grid)={bool(grid)}`'

    # extract polygons
    polygons = feature['geometry']['coordinates']

    # initiate output
    result = dict()

    # skip if none of the grid points is within the polygon
    if quick_check:
        # grid coordinates
        grid_x, grid_y = np.array([*grid.keys()]).T

        # loop over polygons
        grid_in_polygon = False
        for polygon in polygons:
            if len(polygon[0]) == 2:
                # polygon definition
                x, y = zip(*polygon)
            else:
                # multi-polygon definition
                _polygon = []
                for sub_polygon in polygon:
                    _polygon.extend(sub_polygon)
                x, y = zip(*_polygon)

            # any grid-point in square-shaped polygon
            if np.any(((grid_x > min(x)) & (grid_x < max(x))) & ((grid_y > min(y)) & (grid_y < max(y)))):
                grid_in_polygon = True
                break

        # return empty dict if no grid-point in square-shaped polygon
        if not grid_in_polygon:
            return result

    # extract ecotope-label
    label = feature['properties']['zes_code']
    if label == 'overig':
        label = 'xx.xxx'

    # create `shapely.geometry.Polygon`-objects
    polygons = [geometry.Polygon(polygon) for polygon in polygons]

    # determine if points are in stacked polygons
    for point in points:
        # point in separate polygons
        inside_separate = [polygon.contains(point) for polygon in polygons]
        # point in stacked polygons
        inside_stacked = functools.reduce(lambda a, b: a ^ b, inside_separate)
        # append point to result (if in stacked polygons)
        if inside_stacked:
            result[(point.x, point.y)] = label

    # return labeled feature
    return result


def polygon2grid(f_polygon: str, f_grid: str = None, grid: dict = None, **kwargs) -> _TypeXYLabel:
    # optional arguments
    n_cores: int = kwargs.get('n_cores', 1)
    quick_check: bool = kwargs.get('quick_check_grid_in_polygon', False)

    # either `f_grid` or `grid` must be defined
    if not (bool(f_grid) ^ bool(grid)):
        msg = f'Either `f_grid` or `grid` must be defined: `f_grid={f_grid}` and `grid={grid}`'
        raise ValueError(msg)

    # open polygon data
    with open(f_polygon, mode='r') as f:
        data = json.load(f)

    # open grid data
    if f_grid:
        grid = csv2grid(f_grid)

    # grid to `shapely.geometry.Point`-objects
    points = [geometry.Point(xy) for xy in grid]

    # extract features
    features = data['features']

    # add `grid` to `kwargs`
    if quick_check:
        kwargs['grid'] = grid

    # parallel computing: settings
    n_features = data['totalFeatures']
    n_processes = min(n_cores, n_features)
    _LOG.info(f'CPUs made available: {n_cores} / {mp.cpu_count()}')
    _LOG.info(f'CPUs used: {n_processes} / {mp.cpu_count()}')
    _LOG.info(f'CPUs required: {n_features} / {n_processes}')

    # parallel computing: translation
    if n_processes == 1:
        lst_results = [points_in_feature(feature, points, **kwargs) for feature in features]
    else:
        with mp.Pool(processes=n_processes) as p:
            lst_results = p.map(functools.partial(points_in_feature, points=points, **kwargs), features)

    # compress results
    result = {k: v for d in lst_results for k, v in d.items()}

    # return results
    return result
