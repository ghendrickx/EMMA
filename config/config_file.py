"""
Setting the configuration file for the labelling of ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import json
import logging
import os

_LOG = logging.getLogger(__name__)


def load_config(f_default: str, f_user: str = None, wd: str = None) -> dict:
    """Load the default configuration file and update with values from a user-defined configuration file, if applicable.

    :param f_default: default configuration file name
    :param f_user: user-defined configuration file name, defaults to None
    :param wd: working directory, defaults to None

    :type f_default: str
    :type f_user: str, optional
    :type wd: str, optional

    :return: configuration
    :rtype: dict
    """
    # load default configuration
    with open(os.path.join(os.path.dirname(__file__), f_default)) as f:
        default = json.load(f)

    # no user-defined configuration
    if f_user is None:
        _LOG.info(f'Default configuration used: {f_default}')
        return default

    # built-in ZES.1 configuration
    elif f_user in ('zes1.json',):
        with open(os.path.join(os.path.dirname(__file__), f_user)) as f:
            built_in = json.load(f)

        if f_user == 'zes1.json':
            name_built_in = 'ZES.1'
        else:
            msg = f'Unknown name of built-in configuration: {f_user}'
            raise NotImplementedError(msg)

        _LOG.info(f'Built-in {name_built_in} configuration used: {f_user}')
        return built_in

    # custom (partial) configuration
    else:
        wd = wd or os.getcwd()
        file = os.path.join(wd, f_user)
        try:
            with open(file) as f_user:
                user = json.load(f_user)
        except FileNotFoundError:
            _LOG.warning(f'Custom configuration file not found: {file}')
            load_config(f_default, f_user=None, wd=wd)
        else:
            _LOG.info(f'Custom configuration file used: {file}')

    # merge configurations
    default.update(user)
    if user:
        _LOG.warning(f'Default configuration replaced: {user}')

    # return configuration
    return default
