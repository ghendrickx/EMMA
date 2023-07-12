"""
Processing of output data of hydrodynamic model by labelling the ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import functools
import logging
import multiprocessing as mp
import time

import numpy as np
import typing

from config import config_file
from src import labelling as lab, preprocessing as pre, export as exp

_LOG = logging.getLogger(__name__)


def __log_config(part_id: int = None, **kwargs):
    """Set logging configuration.

    :param part_id: partition ID (only for parallel computations), defaults to None
    :param kwargs: optional arguments
        export_log: export log-file, defaults to None
        log_level: level of log-statements printed/filed, defaults to 'warning'
        wd_export: working directory for exporting ecotope map(s), defaults to None

    :type part_id: int, optional
    :type kwargs: optional
        export_log: bool, str
        log_level: str
        wd_export: str
    """
    # optional arguments
    log_level: str = kwargs.get('log_level', 'warning')
    wd_export: str = kwargs.get('wd_export')
    export_log: typing.Union[bool, str] = kwargs.get('export_log', wd_export is not None)

    # set logging configuration
    # logging.shutdown()
    logger = logging.getLogger()
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])
    if export_log:
        log_file = export_log if isinstance(export_log, str) else None
        if part_id is not None:
            if log_file is None:
                log_file = f'emma_{part_id:04d}'
            else:
                log_file = f'{log_file.split(".")[0]}_{part_id:04d}'
        exp.export2log(log_level, file_name=log_file, wd=wd_export)
    else:
        logging.basicConfig(level=log_level.upper())


def map_ecotopes(f_map: typing.Union[str, typing.Sized], **kwargs) -> typing.Union[dict, None]:
    """Map ecotopes from hydrodynamic model data.

    :param f_map: file name of hydrodynamic model output data (*.nc)
    :param kwargs: optional arguments
        f_export: file name for exporting ecotope map(s), defaults to None
        n_cores: number of cores available for parallel computations, defaults to 1
        return_ecotopes: return a dictionary with the ecotopes using (x,y)-coordinates as keys, defaults to True
        wd_export: working directory for exporting ecotope map(s), defaults to None
        optional arguments to `.__log_config()`
        optional arguments to `.__determine_ecotopes()`

    :type f_map: str, typing.Sized
    :type kwargs: optional
        f_export: str
        n_cores: int
        return_ecotopes: bool
        wd_export: str

    :return: spatial distribution of ecotopes (optional)
    :rtype: dict, None

    :raise AssertionError: if `substratum_1` not in {None, 'soft', 'hard'}
    """
    # start time
    t0 = time.perf_counter()

    # set logging configuration
    __log_config(**kwargs)

    # start ecotope-mapper
    _LOG.info(f'Ecotope-map based on {f_map}')

    # optional arguments
    # > export ecotope-data
    wd_export: str = kwargs.get('wd_export')
    return_ecotopes: bool = kwargs.get('return_ecotopes', True)
    f_export: typing.Union[bool, str, None] = kwargs.get('f_export', not return_ecotopes)

    # > parallel computing
    n_cores: int = kwargs.get('n_cores', 1)
    _LOG.info(f'CPUs made available: {n_cores} / {mp.cpu_count()}')

    # extract model data
    if isinstance(f_map, str) or len(f_map) == 1:
        _LOG.info(f'CPUs used: 1 / {mp.cpu_count()}')
        if not isinstance(f_map, str):
            f_map = f_map[0]
        x_coordinates, y_coordinates, ecotopes = __determine_ecotopes(f_map, **kwargs)
    else:
        n_files = len(f_map)
        n_processes = min(n_cores, n_files)
        _LOG.info(f'CPUs used: {n_processes} / {mp.cpu_count()}')
        _LOG.info(f'CPUs required: {n_files} / {n_processes}')

        kwargs.update({'_map_files': list(f_map)})

        with mp.Pool(processes=n_processes) as p:
            results = p.map(functools.partial(__determine_ecotopes, **kwargs), f_map)

        x_coordinates, y_coordinates, ecotopes = [np.concatenate(arrays) for arrays in zip(*results)]

    # export ecotope-data
    if f_export:
        _LOG.warning(f'Currently, only exporting to a *.csv-file is supported.')
        if isinstance(f_export, bool):
            f_export = None
        exp.export2csv(x_coordinates, y_coordinates, ecotopes, file_name=f_export, wd=wd_export)

    # computation time
    t1 = time.perf_counter()
    _LOG.info(f'Ecotope-map generated in {t1 - t0:.4f} seconds')

    # return ecotope-map
    if return_ecotopes:
        return {(x, y): eco for x, y, eco in zip(x_coordinates, y_coordinates, ecotopes)}


def __determine_ecotopes(file_name: str, **kwargs) -> tuple:
    """Map ecotopes from hydrodynamic model data.

    :param f_map: file name of hydrodynamic model output data (*.nc)
    :param kwargs: optional arguments
        chezy: Chezy coefficient, defaults to 50
        export_log: export log-file, defaults to None
        f_eco_config: file name of ecotopes configuration file, defaults to None
        f_export: file name for exporting ecotope map(s), defaults to None
        f_map_config: file name of mapping configuration file, defaults to None
        friction_coefficient: proxy friction coefficient combining `shields`, `chezy`, and `relative_density`,
            defaults to None
        lat: lowest astronomical tide, defaults to None
        log_level: level of log-statements printed/filed, defaults to 'warning'
        mhwn: mean high water, neap tide, defaults to None
        mlws: mean low water, spring tide, defaults to None
        model_sediment: sediment data is included in model output data, defaults to False [not implemented]
        relative_density: relative density of sediment w.r.t. (sea) water, defaults to 1.58
        return_ecotopes: return a dictionary with the ecotopes using (x,y)-coordinates as keys, defaults to True
        shields: critical Shields parameter, defaults to 0.07
        substratum_1: definition of substratum {None, 'soft', 'hard'}, defaults to None
        time_axis: time-axis in model output data, defaults to 0
        wd: working directory, defaults to None
        wd_config: working directory of configuration file(s), defaults to None
        wd_export: working directory for exporting ecotope map(s), defaults to None

    :type f_map: str, typing.Sized
    :type kwargs: optional
        chezy: float
        export_log: bool, str
        f_eco_config: str
        f_export: str
        f_map_config: str
        friction_coefficient: float
        lat: float
        log_level: str
        mhwn: float
        mlws: float
        model_sediment: bool
        relative_density: float
        return_ecotopes: bool
        shields: float
        substratum_1: str
        time_axis: int
        wd: str
        wd_config: str
        wd_export: str

    :return: spatial distribution of ecotopes (optional)
    :rtype: dict, None

    :raise AssertionError: if `substratum_1` not in {None, 'soft', 'hard'}
    """
    # partition ID
    _map_files: list = kwargs.pop('_map_files', False)
    part_id = _map_files.index(file_name) if _map_files else None

    # set logging configuration
    __log_config(part_id, **kwargs)

    # optional arguments
    wd = kwargs.get('wd')
    time_axis: int = kwargs.get('time_axis', 0)
    model_sediment: bool = kwargs.get('model_sediment', False)

    # > configuration file
    wd_config: str = kwargs.get('wd_config')
    eco_config: str = kwargs.get('f_eco_config')
    map_config: str = kwargs.get('f_map_config')

    # > substratum 1
    substratum_1: str = kwargs.get('substratum_1')
    assert substratum_1 in (None, 'soft', 'hard')
    _LOG.warning(f'`substratum_1` is uniformly applied: \"{substratum_1}\"')

    # > substratum 2
    shields: float = kwargs.get('shields', .07)
    chezy: float = kwargs.get('chezy', 50)
    r_density: float = kwargs.get('relative_density', 1.58)
    c_friction: float = kwargs.get('friction_coefficient')
    # >> calibrated `c_friction`-value
    if eco_config in (None, 'emma.json') and substratum_1 == 'soft':
        c_friction = c_friction or 1300

    # > tidal characteristics
    mlws: float = kwargs.get('mlws')
    mhwn: float = kwargs.get('mhwn')
    if mlws is None or mhwn is None:
        _LOG.warning(f'Not all relevant tidal characteristics are provided: `mlws={mlws}` [m]; `mhwn={mhwn}` [m]')
        _LOG.info(f'Hard-coded values in the configuration-file ({eco_config or "emma.json"}) are used')
    lat: float = kwargs.get('lat')
    if lat is None and eco_config not in ('zes1.json',):
        _LOG.warning(
            f'Lowest astronomical tide (LAT) not provided (`lat={lat}` [m])`; '
            f'defaulting to mean low water, spring tide (MLWS, `mlws={mlws}` [m]) with reduced performance`'
        )
        lat = mlws

    # set configurations
    # > ecotope configuration
    lab.CONFIG = config_file.load_config('emma.json', eco_config, wd_config)
    # > map configuration
    pre.CONFIG = config_file.load_config('dfm2d.json', map_config, wd_config)

    # extract model data
    data = pre.MapData(file_name, wd=wd)
    x_coordinates = data.x_coordinates
    y_coordinates = data.y_coordinates
    water_depth = data.water_depth
    if np.mean(water_depth) < 0:
        _LOG.warning(
            'Average water depth is negative, while water depth is considered positive downwards. '
            'Check the model configuration and update the configuration file accordingly.'
        )
    velocity = data.velocity
    salinity = data.salinity
    if model_sediment:
        _LOG.warning('Retrieving grain sizes from the model not implemented')
        grain_sizes = data.grain_size
    else:
        grain_sizes = None
    data.close()

    # pre-process model data
    mean_salinity, std_salinity = pre.process_salinity(salinity, time_axis=time_axis)
    mean_depth, in_duration, in_frequency = pre.process_water_depth(water_depth, time_axis=time_axis)
    med_velocity, max_velocity = pre.process_velocity(velocity, time_axis=time_axis)
    if grain_sizes is None:
        grain_sizes = pre.grain_size_estimation(
            med_velocity, shields=shields, chezy=chezy, r_density=r_density, c_friction=c_friction
        )
    _LOG.info('Model data pre-processed')

    # ecotope-labelling
    char_1 = np.vectorize(lab.salinity_code)(mean_salinity, std_salinity)
    # noinspection PyTypeChecker
    char_2 = np.full_like(char_1, lab.substratum_1_code(substratum_1), dtype=str)
    char_3 = np.vectorize(lab.depth_1_code)(mean_depth, lat, mhwn)
    char_4 = np.vectorize(lab.hydrodynamics_code)(max_velocity, char_3)
    char_5 = np.vectorize(lab.depth_2_code)(char_2, char_3, mean_depth, in_duration, in_frequency, mlws)
    char_6 = np.vectorize(lab.substratum_2_code)(char_2, char_4, grain_sizes)

    ecotopes = [
        f'{c1}{c2}.{c3}{c4}{c5}{c6}'
        for c1, c2, c3, c4, c5, c6
        in zip(char_1, char_2, char_3, char_4, char_5, char_6)
    ]
    _LOG.info(f'Ecotopes defined: {len(ecotopes)} instances; {len(np.unique(ecotopes))} unique ecotopes')

    # reset logging
    logging.shutdown()

    # return (x,y)-coordinates and ecotopes
    return x_coordinates, y_coordinates, ecotopes
