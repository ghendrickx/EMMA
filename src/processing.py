"""
Processing of output data of hydrodynamic model by labelling the ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging

import numpy as np

from config import config_file
from src import labelling as lab, preprocessing as pre

_LOG = logging.getLogger(__name__)


def map_ecotopes(file_name: str, wd: str=None, **kwargs) -> dict:
    """Map ecotopes from hydrodynamic model data.

    :param file_name:
    :param wd:
    :param kwargs:
    :return:
    """
    # optional arguments
    time_axis = kwargs.get('time_axis', 0)
    model_sediment = kwargs.get('model_sediment', False)
    substratum_1 = kwargs.get('substratum_1')

    # substratum 1
    assert substratum_1 in (None, 'soft', 'hard')
    _LOG.warning(f'`substratum 1` is uniformly applied: \"{substratum_1}\"')

    # substratum 2
    shields = kwargs.get('shields', .03)
    chezy = kwargs.get('chezy', 60)
    r_density = kwargs.get('relative_density', 1.58)
    c_friction = kwargs.get('friction_coefficient')

    # set configuration file
    f_config = kwargs.get('config_file')
    wd_config = kwargs.get('config_wd')
    lab.CONFIG = config_file.load_config(f_config, wd_config)

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

    # ecotope-labelling
    char_1 = np.vectorize(lab.salinity_code)(mean_salinity, std_salinity)
    # noinspection PyTypeChecker
    char_2 = np.full_like(char_1, lab.substratum_1_code(substratum_1), dtype=str)
    char_3 = np.vectorize(lab.depth_1_code)(in_duration)
    char_4 = np.vectorize(lab.hydrodynamics_code)(max_velocity, char_3)
    char_5 = np.vectorize(lab.depth_2_code)(char_2, char_3, mean_depth, in_duration, in_frequency)
    char_6 = np.vectorize(lab.substratum_2_code)(char_2, char_4, grain_sizes)

    ecotopes = [
        f'{c1}{c2}.{c3}{c4}{c5}{c6}'
        for c1, c2, c3, c4, c5, c6
        in zip(char_1, char_2, char_3, char_4, char_5, char_6)
    ]

    # return ecotope-map
    return {(x, y): eco for x, y, eco in zip(x_coordinates, y_coordinates, ecotopes)}
