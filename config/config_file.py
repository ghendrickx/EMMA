"""
Setting the configuration file for the labelling of ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import json
import logging
import os

import typing

_LOG = logging.getLogger(__name__)


def load_config(f_default: str, f_user: typing.Union[str, dict] = None, wd: str = None) -> dict:
    """Load the default configuration file and update with values from a user-defined configuration file, if applicable.
    The user-defined configuration can also be provided as a dictionary in which case the user must make sure to match
    the keywords of the dictionary with the keywords of the configuration file.

    :param f_default: default configuration file name
    :param f_user: user-defined configuration (file name), defaults to None
    :param wd: working directory, defaults to None

    :type f_default: str
    :type f_user: str, dict, optional
    :type wd: str, optional

    :return: configuration
    :rtype: dict
    """
    # load default configuration
    with open(os.path.join(os.path.dirname(__file__), f_default), mode='r') as f:
        default = json.load(f)

    # no user-defined configuration
    if f_user is None:
        _LOG.info(f'Default configuration used: {f_default}')
        return default

    # built-in configurations
    if f_user in ('emma.json', 'zes1.json', 'dfm1.json', 'dfm4.json'):
        with open(os.path.join(os.path.dirname(__file__), f_user), mode='r') as f:
            built_in = json.load(f)
        _LOG.info(f'Built-in configuration used: {f_user}')
        return built_in

    # custom (partial) configuration
    if isinstance(f_user, str):
        wd = wd or os.getcwd()
        file = os.path.join(wd, f_user)
        with open(file, mode='r') as f:
            user = json.load(f)

    elif isinstance(f_user, dict):
        user = f_user.copy()

    else:
        msg = f'User-defined configuration must be either a `str` (referring to a JSON-file), ' \
            f'or a `dict` matching the configuration-keywords; {type(f_user)} given'
        raise TypeError(msg)

    # merge configurations
    default = _update_nested_dict(default, user)
    if user:
        _LOG.warning(f'Default configuration replaced: {user}')

    # return configuration
    return default


def _update_nested_dict(d1: dict, d2: dict) -> dict:
    """Update nested dictionary without removing non-updated keys/values.

    :param d1: dictionary to be updated
    :param d2: (partial) dictionary with updated keys/values

    :type d1: dict
    :type d2: dict

    :return: updated, complete dictionary
    :rtype: dict
    """
    # copy dictionaries
    d1 = d1.copy()
    d2 = d2.copy()

    # update dictionary
    for k, v in d2.items():
        if k in d1:
            d1[k] = _update_nested_dict(d1[k], v) if isinstance(v, dict) else v

    # return updated dictionary
    return d1
