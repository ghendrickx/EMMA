"""
Setting the configuration file for the labelling of ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import json
import logging
import os

_LOG = logging.getLogger(__name__)


def load_config(file_name: str = None, wd: str = None) -> dict:
    """Load the default configuration file and update with values from a user-defined configuration file, if applicable.

    :param file_name: configuration file name, defaults to None
    :param wd: working directory, defaults to None

    :type file_name: str, optional
    :type wd: str, optional

    :return: label configuration
    :rtype: dict
    """
    # load default configuration
    with open(os.path.join(os.path.dirname(__file__), 'emma.json')) as f_default:
        default = json.load(f_default)

    # no user-defined configuration
    if file_name is None:
        user = {}
        _LOG.info(f'Default configuration used: emma.json')

    # built-in ZES.1 configuration
    elif file_name in ('zes1.json',):
        with open(os.path.join(os.path.dirname(__file__), file_name)) as f_builtin:
            user = json.load(f_builtin)
        _LOG.info(f'Built-in ZES.1 configuration used: zes1.json')

    # custom (partial) configuration
    else:
        wd = wd or os.getcwd()
        file = os.path.join(wd, file_name)
        try:
            with open(file) as f_user:
                user = json.load(f_user)
        except FileNotFoundError:
            _LOG.warning(f'Custom configuration file not found: \"{file}\".')
            user = {}
        else:
            _LOG.info(f'Custom configuration file used: file')

    # merge configurations
    default.update(user)
    if user:
        _LOG.warning(f'Default configuration replaced: {user}')

    # return configuration
    return default
