"""
Export ecotope-map.

Author: Gijs G. Hendrickx
"""
import logging
import os

import typing

_LOG = logging.getLogger(__name__)


def _file_name(default: str, extension: str = None) -> callable:
    """Decorator to define default file name and log the file-location of the exported data.

    :param default: default file name
    :param extension: file extension, defaults to None

    :type default: str
    :type extension: str, optional

    :return: decorator function
    :rtype: callable
    """

    def decorator(func: callable) -> callable:
        """Decorator function."""

        def wrapper(*args, **kwargs) -> None:
            """Wrapper function."""
            # export settings
            file_name = _default_file_name(kwargs.pop('file_name', None), default=default, extension=extension)
            wd = kwargs.pop('wd', os.getcwd())

            # function execution
            func(*args, file_name=file_name, wd=wd, **kwargs)

            # logging
            _LOG.info(f'Data exported: {os.path.join(wd, file_name)}')

        # return wrapper function
        return wrapper

    # return decorator function
    return decorator


def _default_file_name(file_name: str, default: str, extension: str = None):
    """Use default file name if none is defined. The extension is based on the default file name provided if not stated
    explicitly.

    :param file_name: file name
    :param default: default file name
    :param extension: file extension, defaults to None

    :type file_name: str, None
    :type default: str
    :type extension: str, optional

    :return: file name
    :rtype: str
    """
    if file_name is None:
        _LOG.info(f'Default file-name used: {default}')
        return default

    if extension is None:
        extension = f'.{default.split(".")[-1]}'
    elif not extension.startswith('.'):
        extension = f'.{extension}'

    if not file_name.endswith(extension):
        return f'{file_name.split(".")[0]}{extension}'

    return file_name


@_file_name(default='ecotopes.csv')
def export2csv(
        x: typing.Sized, y: typing.Sized, ecotopes: typing.Sized, *, file_name: str = None, wd: str = None
) -> None:
    """Export ecotope-map to a *.csv-file, containing the x- and y-coordinates and their corresponding ecotope
    (prediction).

    :param x: x-coordinates
    :param y: y-coordinates
    :param ecotopes: ecotope distribution data
    :param file_name: file name, defaults to None
    :param wd: working directory, defaults to None

    :type x: iterable
    :type y: iterable
    :type ecotopes: iterable
    :type file_name: str, optional
    :type wd: str, optional
    """
    assert len(x) == len(y) == len(ecotopes)

    # file specifications
    file = os.path.join(wd, file_name)

    # export data
    with open(file, mode='w') as f:
        for xi, yi, ei in zip(x, y, ecotopes):
            f.write(f'{xi},{yi},{ei}\n')


@_file_name(default='ecotopes.nc')
def export2nc(data: dict, *, file_name: str, wd: str = None) -> None:
    """Export ecotope-map data to a netCDF-file, containing x-, y-, and ecotope-data.

    :param data:
    :param file_name:
    :param wd:
    :return:
    """
    return NotImplemented
