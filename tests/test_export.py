"""
Tests for `src/export.py`.

Author: Gijs G. Hendrickx
"""
import os

import pytest

from src import export as exp


@pytest.mark.parametrize(
    'file_name, wd, expected',
    [
        ('C:/Users/me/Documents/file.txt', None, 'C:/Users/me/Documents/file.txt'),
        ('D:/folder/file.txt', None, 'D:/folder/file.txt'),
        ('P:/folder/file.txt', None, 'P:/folder/file.txt'),
        ('~/folder/file.txt', None, '~/folder/file.txt'),
        ('/folder/file.txt', None, '/folder/file.txt'),
        (r'\folder\file.txt', None, r'\folder\file.txt'),
        ('file.txt', None, os.path.join(os.getcwd(), 'file.txt'))
    ]
)
def test_file_dir(file_name, wd, expected):
    file = exp.file_dir(file_name, wd)
    assert file == expected


@pytest.mark.parametrize(
    'file_name, default, extension, expected',
    [
        ('file.txt', 'f.txt', None, 'file.txt'),
        ('file', 'f.txt', None, 'file.txt'),
        ('file', 'f.txt', '.csv', 'file.csv'),
        ('file.csv', 'f.txt', '.txt', 'file.txt'),
        ('file', 'f.txt', 'txt', 'file.txt'),
        ('file.txt', 'f_net.txt', '_net.txt', 'file_net.txt'),
    ]
)
def test_default_file_name(file_name, default, extension, expected):
    file = exp._default_file_name(file_name, default, extension)
    assert file == expected
