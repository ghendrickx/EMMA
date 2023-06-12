"""
Setting the configuration file for the labelling of ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import json
import logging
import os

_LOG = logging.getLogger(__name__)


def load_config(file_name: str=None, wd: str=None) -> dict:
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

    # load user-defined configuration
    if file_name is None:
        user = {}
    else:
        wd = wd or os.getcwd()
        file = os.path.join(wd, file_name)
        try:
            with open(file) as f_user:
                user = json.load(f_user)
        except FileNotFoundError:
            _LOG.warning(f'configuration file not found: {file}')
            user = {}

    # merge configuration files
    default.update(user)

    # return configuration
    return default
