"""
Processing of output data of hydrodynamic model by labelling the ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging
import time

import numpy as np
import typing

from config import config_file
from src import labelling as lab, preprocessing as pre, export as exp

_LOG = logging.getLogger(__name__)


def map_ecotopes(file_name: str, wd: str = None, **kwargs) -> typing.Union[dict, None]:
    """Map ecotopes from hydrodynamic model data.

    :param file_name: file name of hydrodynamic model output data (*.nc)
    :param wd: working directory, defaults to None
    :param kwargs: optional arguments

    :type file_name: str
    :type wd: str, optional
    :type kwargs: optional

    :return: spatial distribution of ecotopes (optional)
    """
    # start time
    t0 = time.perf_counter()

    # optional arguments
    time_axis: int = kwargs.get('time_axis', 0)
    model_sediment: bool = kwargs.get('model_sediment', False)

    # > configuration file
    wd_config: str = kwargs.get('wd_config')
    eco_config: str = kwargs.get('f_eco_config')
    map_config: str = kwargs.get('f_map_config')

    # > export ecotope-data
    f_export: str = kwargs.get('f_export')
    wd_export: str = kwargs.get('wd_export')
    return_ecotopes: bool = kwargs.get('return_ecotopes', True)

    # > set logging configuration
    export_log: bool = kwargs.get('export_log', True)
    if export_log:
        log_file = export_log if isinstance(export_log, str) else None
        exp.export2log(kwargs.get('log_level', 'warning'), file_name=log_file, wd=wd_export)

    # > substratum 1
    substratum_1: str = kwargs.get('substratum_1')
    assert substratum_1 in (None, 'soft', 'hard')
    _LOG.warning(f'`substratum 1` is uniformly applied: \"{substratum_1}\".')

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
        _LOG.warning(
            f'Not all relevant tidal characteristics are provided: `mlws={mlws}` [m]; `mhwn={mhwn}` [m]. '
            f'If not provided, the hard-coded values in the configuration-file ({eco_config or "emma.json"}) are used.'
        )
    lat: float = kwargs.get('lat')
    if lat is None and eco_config not in ('zes1.json',):
        _LOG.warning(
            f'Lowest astronomical tide (LAT) not provided (`lat={lat}` [m])`; '
            f'defaulting to mean low water, spring tide (MLWS, `mlws={mlws}` [m]) with reduced performance`.'
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
    velocity = data.velocity
    salinity = data.salinity
    if model_sediment:
        _LOG.warning('Retrieving grain sizes from the model not implemented.')
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
    _LOG.info(f'Model data pre-processed')

    # ecotope-labelling
    char_1 = np.vectorize(lab.salinity_code)(mean_salinity, std_salinity)
    #       noinspection PyTypeChecker
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

    # export ecotope-data
    if f_export:
        _LOG.warning(f'Currently, only exporting to a *.csv-file is supported.')
        exp.export2csv(x_coordinates, y_coordinates, ecotopes, file_name=f_export, wd=wd_export)

    # logging
    t1 = time.perf_counter()
    _LOG.info(f'Ecotope-map generated in {t1 - t0:.4f} seconds')

    # return ecotope-map
    if return_ecotopes:
        return {(x, y): eco for x, y, eco in zip(x_coordinates, y_coordinates, ecotopes)}
