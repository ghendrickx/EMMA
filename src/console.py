"""
Run EMMA from the command-line.

Author: Gijs G. Hendrickx
"""
import sys
import time
import typing

import typer
import typing_extensions as te

from src import processing, performance

# EMMA-application
app_emma = typer.Typer()


def __log_levels(log: str) -> str:
    """Callback function for allowed log-levels.

    :param log: log-level
    :type log: str

    :return: log-level
    :rtype: str
    """
    # capitalise all strings
    log = log.upper()
    levels = 'DEBUG', 'INFO', 'WARNING', 'CRITICAL'

    # verify validity of `log`-argument
    if log not in levels:
        msg = f'Unknown log-level, {log}; choose one of {levels}'
        raise typer.BadParameter(msg)

    # return log-level
    return log


def __print_statements() -> None:
    """Print copyright-statements."""
    print(
        '\nEMMA  Copyright (c)  EMMA Development Team\n'
        'This program comes with NO WARRANTY.\n'
        'This is free software, and you are welcome to use and redistribute it\n'
        'under the conditions as specified in the license; see LICENSE (Apache 2.0)\n',
        file=sys.stderr
    )


# noinspection PyUnresolvedReferences
@app_emma.command(name='run', help='execution of EMMA with customisation of the basic optional arguments')
def run(
        map_files: te.Annotated[typing.List[str], typer.Argument(help='hydrodynamic output map-file(s)')],
        export: te.Annotated[bool, typer.Option(help='export model data to [wd]')] = True,
        f_eco_config: te.Annotated[str, typer.Option(help='ecotope configuration file')] = 'emma.json',
        f_map_config: te.Annotated[str, typer.Option(help='map configuration file')] = 'dfm1.json',
        log: te.Annotated[str, typer.Option(
            '--log', '-l', autocompletion=__log_levels, callback=__log_levels, help='level of log statements'
        )] = 'WARNING',
        n_cores: te.Annotated[int, typer.Option(
            '--cores', '-n', min=1, help='number of cores for parallel computation'
        )] = 1,
        wd: te.Annotated[str, typer.Option(help='working directory')] = None,
) -> None:
    """Run EMMA with limited modifications from the command-line. For the full spectrum of customisation, EMMA should be
    executed using Python, and calling the `src.processing.map_ecotopes`-function.

    :param map_files: file name(s) of hydrodynamic model output data (*.nc)
    :param export: export data, defaults to True
    :param f_eco_config: file name of ecotopes configuration file, defaults to 'emma.json'
    :param f_map_config: file name of mapping configuration file, defaults to 'dfm1.json'
    :param log: log-level {'DEBUG', 'INFO', 'WARNING', 'CRITICAL'}, defaults to 'WARNING'
    :param n_cores: number of cores available for parallel computations, defaults to 1
    :param wd: working directory, defaults to None

    :type map_files: list[str]
    :type export: bool, optional
    :type f_eco_config: str, optional
    :type f_map_config: str, optional
    :type log: str, optional
    :type n_cores: int, optional
    :type wd: str, optional
    """
    __print_statements()
    # noinspection PyArgumentList
    processing.map_ecotopes(
        *map_files,
        f_export=export,
        f_eco_config=f_eco_config,
        f_map_config=f_map_config,
        export_log=export,
        log_level=log,
        n_cores=n_cores,
        wd=wd,
        wd_config=wd,
        wd_export=wd,
    )


# noinspection PyUnresolvedReferences
@app_emma.command(name='compare', help='[NOT YET IMPLEMENTED] compare EMMA predictions to existing ecotope-maps')
def compare(
        f_data: te.Annotated[str, typer.Argument(
            help='file with ecotope polygon (validation) data (*.json/*.csv-file)'
        )],
        f_emma: te.Annotated[str, typer.Argument(help='file with ecotope grid data from EMMA (*.csv-file)')],
        level: te.Annotated[int, typer.Option(min=0, max=6, help='level of detail of comparison')] = None,
        n_cores: te.Annotated[int, typer.Option(
            '--cores', '-n', min=1, help='number of cores for parallel computation'
        )] = 1,
        wd: te.Annotated[str, typer.Option(help='working directory')] = None,
) -> None:
    """Compare predictions of ecotopes based on EMMA with existing polygon-data of ecotopes.

    :param map_files: file name(s) of hydrodynamic model output data (*.nc)
    :param f_ecotopes: file name of ecotope-polygon data
    :param level: level of detail of comparison, defaults to None
    :param n_cores: number of cores for parallel computation, defaults to 1
    :param wd: working directory, defaults to None

    :type f_data: str
    :type f_emma: str
    :type level: int, optional
    :type n_cores: int, optional
    :type wd: str, optional
    """
    __print_statements()
    # noinspection PyTypeChecker
    performance.execute(
        f_data,
        f_emma,
        level=level,
        n_cores=n_cores,
        wd=wd
    )


@app_emma.command(name='test', help='test if EMMA and her dependencies are installed properly')
def test() -> None:
    """EMMA-call testing the installation of all dependencies."""
    try:
        from src import _globals, export, labelling, performance, preprocessing, processing
        from config import config_file
    except ImportError:
        print('\nEMMA and her dependencies are NOT installed properly.\n')
        sys.exit(1)
    else:
        print('\nEMMA and her dependencies are installed properly.\n')


if __name__ == '__main__':
    # Execute the EMMA-application.
    app_emma()
