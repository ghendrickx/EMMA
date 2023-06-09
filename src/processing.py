"""
Processing of output data of hydrodynamic model by labelling the ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging

import numpy as np

from src import labelling as lab, preprocessing as pre


_LOG = logging.getLogger(__name__)


def vectorised_labelling(func: callable, *args) -> np.char.array:
    """Vectorised execution of ecotope-code determination functions, translating the string-containing arrays to
    `np.char.array` for efficient further processing.

    :param func: ecotope-code determination function
    :param args: function's arguments

    :type func: callable
    :type args: numpy.ndarray, float, str

    :return: partial ecotope-codes
    :rtype: numpy.char.array
    """
    return np.char.array(np.vectorize(func)(*args))


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

    shields = kwargs.get('shields', .03)
    chezy = kwargs.get('chezy', 60)
    r_density = kwargs.get('relative_density', 1.58)

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
    min_salinity, mean_salinity, max_salinity = pre.process_salinity(salinity, time_axis=time_axis)
    in_duration, in_frequency = pre.process_water_depth(water_depth, time_axis=time_axis)
    med_velocity, max_velocity = pre.process_velocity(velocity, time_axis=time_axis)
    if grain_sizes is None:
        grain_sizes = pre.grain_size_estimation(med_velocity, shields=shields, chezy=chezy, r_density=r_density)

    # ecotope-labelling
    char_1 = vectorised_labelling(lab.salinity_code, mean_salinity, min_salinity, max_salinity)
    char_2 = lab.substratum_1_code(substratum_1)
    char_3 = vectorised_labelling(lab.depth_1_code, in_duration)
    char_4 = vectorised_labelling(lab.hydrodynamics_code, max_velocity, char_3)
    char_5 = vectorised_labelling(lab.depth_2_code, char_2, char_3, in_duration, in_frequency)
    char_6 = vectorised_labelling(lab.substratum_2_code, char_2, char_4, grain_sizes)

    ecotopes = char_1 + char_2 + char_3 + char_4 + char_5 + char_6

    # return ecotope-map
    return {(x, y): eco for x, y, eco in zip(x_coordinates, y_coordinates, ecotopes)}
