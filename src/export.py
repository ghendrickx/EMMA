"""
Export ecotope-map.

Author: Gijs G. Hendrickx
"""
import os

import typing


def _file_extension(file_name: str, file_ext: str) -> str:
    """Assure the correct file extension.

    :param file_name: file name
    :param file_ext: file extension

    :type file_name: str
    :type file_ext: str

    :return: file name with correct extension
    :rtype: str
    """
    # correct file extension
    if file_name.endswith(file_ext):
        return file_name

    # enforce file extension
    f = file_name.split('.')[0]
    return f'{f}.{file_ext}'


def export2csv(x: typing.Sized, y: typing.Sized, ecotopes: typing.Sized, file_name: str = None, wd: str = None) -> None:
    """Export ecotope-map to a *.csv-file, containing the x- and y-coordinates and their corresponding ecotope
    (prediction).

    :param x: x-coordinates
    :param y: y-coordinates
    :param ecotopes: ecotope distribution data
    :param file_name: file name
    :param wd: working directory, defaults to None

    :type x: iterable
    :type y: iterable
    :type ecotopes: iterable
    :type file_name: str
    :type wd: str, optional
    """
    assert len(x) == len(y) == len(ecotopes)

    # file specifications
    file_name = _file_extension(file_name or 'ecotopes', 'csv')
    wd = wd or os.getcwd()
    file = os.path.join(wd, file_name)

    # export data
    with open(file, mode='w') as f:
        for xi, yi, ei in zip(x, y, ecotopes):
            f.write(f'{xi},{yi},{ei}\n')


def export2nc(data: dict, file_name: str, wd: str = None) -> None:
    """Export ecotope-map data to a netCDF-file, containing x-, y-, and ecotope-data.

    :param data:
    :param file_name:
    :param wd:
    :return:
    """
    return NotImplemented
