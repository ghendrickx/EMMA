"""
Performance of EMMA with respect to existing ecotope-maps.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import functools
import json
import logging
import multiprocessing as mp
import typing

import numpy as np

from shapely import geometry

from src import _globals as glob

_LOG = logging.getLogger(__name__)


class Comparison:
    """Compare ecotope-map(s) considered as ground-truth to the map(s) as predicted by `EMMA` from hydrodynamic model
    results.
    """
    _TypeXYLabel = glob.TypeXYLabel

    def __init__(self, data: _TypeXYLabel, model: _TypeXYLabel, **kwargs) -> None:
        """Both `data` and `model` must be formatted as follows: (x,y)-coordinates as key, and the ecotope-label as
        value (`str`). This corresponds with the formatting of the returned `dict` by `map_ecotopes()` (from
        `src.processing`).
        >>> data = {
        ...     (0, 0): 'Z2.222f',
        ... }

        :param data: ground-truth ecotope-labels
        :param model: predicted ecotope-labels
        :param kwargs: optional arguments
            wild_card: wild-card character in ecotope-labels, defaults to 'x'

        :type data: dict[tuple[float, float], str]
        :type model: dict[tuple[float, float], str]
        :type kwargs: optional
            wild_card: str
        """
        # initiate required arguments
        self._data = data
        self._model = model

        # initiate optional arguments
        self.wild_card: str = kwargs.get('wild_card', 'x')

        # non-overlapping data
        if not all(k in data for k in model):
            _LOG.warning('Not all (x,y)-coordinates in `model` are present in `data`')
        if not all(k in model for k in data):
            _LOG.warning('Not all (x,y)-coordinates in `data` are present in `model`')

    @property
    def data(self) -> _TypeXYLabel:
        """
        :return: ground-truth ecotope-labels
        :rtype: dict[tuple[float, float], str]
        """
        return self._data

    @property
    def model(self) -> _TypeXYLabel:
        """
        :return: predicted ecotope-labels
        :rtype: dict[tuple[float, float], str]
        """
        return self._model

    def exec(self, level: typing.Union[int, None], **kwargs) -> glob.TypeXYBool:
        """Execute the comparison up to a given level of detail. This level of detail reflects the number of label-
        components (i.e., letters or numbers) to assess, starting from the left. Note that this excludes any dots (.) in
        the labels. In case the `specific_label` is enabled, `level` reflects the index of the label-component to
        assess. Thus, with `specific_label` disabled (default), the labels are assessed as `label[:level]`; and with
        `specific_label` enabled, the labels are assessed as `label[level]`.

        Ecotope-labels may contain wild cards (default: 'x'), which may represent any letter or number of the ecotope-
        label. Thus, 'Z2.222f' and 'Z2.222x' are considered a match. This type of assessment can be disabled by setting
        the optional argument `enable_wild_card=False` (default: True).

        :param level: level of assessment, when `None` full assessment is executed
        :param kwargs: optional arguments
            enable_wild_card: the wild card character reflects a match, defaults to True
            specific_label: assess a specific label only (defined by `level`), defaults to False

        :type level: int
        :type kwargs: optional
            enable_wild_card: bool
            specific_label: bool

        :return: spatial distribution of matching ecotope-labels
        :rtype: dict[tuple[float, float], bool]

        :raises ValueError: if `level` exceeds ecotope-label components (if `specific_label=True`)
        :raises ValueError: if `level` is negative
        :raises AssertionError: if (x,y)-coordinates, ground-truth ecotope-labels, and predicted ecotope-labels have
            mismatching sizes
        """
        # optional arguments
        enable_wild_card: bool = kwargs.get('enable_wild_card', True)
        specific_label: bool = kwargs.get('specific_label', False)

        # full assessment
        if level is None:
            level = 6

        # check validity `level`-argument
        if specific_label and (not 0 <= level <= 5):
            msg = f'Ecotope-labels consists of six (6) items; ' \
                f'specific label comparison at index {level} is out of range'
            raise ValueError(msg)
        if level < 0:
            msg = f'Level of comparison must be positive, negative value given: {level}'
            raise ValueError(msg)

        # filter and pack data: only (x,y)-coordinates present in data
        filtered = [(k, v, self.model[k]) for k, v in self.data.items() if k in self.model]

        # unpack filtered data
        xy, data, model = zip(*filtered)
        assert len(xy) == len(data) == len(model), \
            f'Sizes of (x,y)-coordinates, ground-truth ecotope-labels, and predicted ecotope-labels must be equal; ' \
            f'respective sizes are {len(xy)}, {len(data)}, and {len(model)}'

        # decompose labels
        data = np.array(data).view('U1').reshape(len(data), -1)
        model = np.array(model).view('U1').reshape(len(model), -1)

        # remove dot from labels (if present)
        data = data[:, ~np.all(data == '.', axis=0)]
        model = model[:, ~np.all(model == '.', axis=0)]

        # append empty string to match label-sizes (if required)
        if data.shape < model.shape:
            data = np.append(data, np.empty((len(data), 1), dtype=str), axis=1)
        elif data.shape > model.shape:
            model = np.append(model, np.empty((len(model), 1), dtype=str), axis=1)

        # compare labels
        wild_card = self.wild_card if enable_wild_card else False
        if specific_label:
            result = (data[:, level] == model[:, level]) | (data[:, level] == wild_card)
        else:
            result = np.all((data[:, :level] == model[:, :level]) | (data[:, :level] == wild_card), axis=1)

        # return spatial performance
        return dict(zip(xy, result))


def csv2grid(file: str) -> glob.TypeXYLabel:
    """Transform *.csv-file with (x, y, label)-data to {(x, y): label}-formatted data.

    :param file: *.csv-file
    :type file: str

    :return: spatial distribution of ecotope-labels
    :rtype: src._globals.TypeXYLabel

    :raises ValueError: if *.csv-file does not contain three (3) columns: x, y, label
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


def points_in_feature(feature: dict, points: typing.Collection[geometry.Point], **kwargs) -> glob.TypeXYLabel:
    """Determine per feature if the grid-points are within the feature's polygon. If so, assign the ecotope-label of the
    feature to these grid-points. A collection of the grid-points that are within the feature's polygon (incl. the
    feature's ecotope-label) are returned.

    :param feature: polygon-based description of spatial distribution of an ecotope
    :param points: grid-points from the hydrodynamic model as a collection of `shapely.geometry.Point`-objects
    :param kwargs: optional arguments
        quick_check: perform a crude check if the grid-points can be within the polygon by drawing a rectangle around
            the polygon, defaults to False

    :type feature: dict
    :type points: collection[shapely.geometry.Point]
    :type kwargs: optional
        quick_check: bool

    :return: labeled grid-points in feature
    :rtype: src._globals.TypeXYLabel
    """
    # optional arguments
    quick_check: bool = kwargs.get('quick_check', False)

    # extract polygons
    polygons = feature['geometry']['coordinates']

    # initiate output
    result = dict()

    # skip if none of the grid points is within the squared polygon
    if quick_check and not _quick_pif(points, polygons):
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


def _quick_pif(points: typing.Collection[geometry.Point], polygons: list) -> bool:
    """Perform a quick check whether the grid-points are within the polygon by squaring the polygon.

    :param points: grid-points from the hydrodynamic model as a collection of `shapely.geometry.Point`-objects
    :param polygons: polygon-definitions

    :type points: collection[shapely.geometry.Point]
    :type polygons: list

    :return: quick-check
    :rtype: bool
    """
    # grid coordinates
    grid_x = np.array([p.x for p in points])
    grid_y = np.array([p.y for p in points])

    # loop over polygons
    grid_in_polygon = False
    for polygon in polygons:
        if len(polygon[0]) > 2:
            polygon = sum(lst for lst in polygon)
        x, y = zip(*polygon)

        # any grid-point in square shaped polygon
        if np.any(((grid_x > min(x)) & (grid_x < max(x))) & ((grid_y > min(y)) & (grid_y < max(y)))):
            grid_in_polygon = True
            break

    return grid_in_polygon


def polygons2grid(f_polygons: str, f_grid: str = None, grid: glob.TypeXY = None, **kwargs) -> glob.TypeXYLabel:
    """Transform polygon data to grid-points by determining which grid-points are within every polygon.

    :param f_polygons: file name of polygon-data
    :param f_grid: file name of grid-data, defaults to None
    :param grid: grid-data, defaults to None
    :param kwargs: optional arguments
        n_cores: number of cores available for parallel computing, defaults to 1
        quick_check: perform a crude check if the grid-points can be within a polygon by drawing a rectangle around the
            polygon, defaults to False

    :type f_polygons: str
    :type f_grid: str, optional
    :type grid: src._globals.TypeXY, optional
    :type kwargs: optional
        n_cores: int
        quick_check: bool

    :return: spatial distribution of ecotope-labels
    :rtype: src._globals.TypeXYLabel

    :raises ValueError: if both or none of `f_grid` and `grid` are defined
    """
    # optional arguments
    n_cores: int = kwargs.get('n_cores', 1)
    quick_check: bool = kwargs.get('quick_check', False)
    _LOG.debug(f'Quick-check executed: {quick_check}')

    # either `f_grid` or `grid` must be defined
    if not bool(f_grid) ^ bool(grid):
        msg = f'Either `f_grid` or `grid` must be defined: `f_grid={f_grid}` and `grid={grid}`'
        raise ValueError(msg)

    # open polygon data
    with open(f_polygons, mode='r') as f:
        data = json.load(f)

    # open grid data
    if f_grid:
        grid = csv2grid(f_grid)

    # grid to `shapely.geometry.Point`-objects
    points = [geometry.Point(xy) for xy in grid]

    # extract features
    features = data['features']

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
    return {k: v for d in lst_results for k, v in d.items()}
