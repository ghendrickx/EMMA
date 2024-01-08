"""
Run EMMA from the command-line.

Author: Gijs G. Hendrickx
"""
import os
import sys
import typing

import typer
import typing_extensions as te

from src import processing

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
        'EMMA  Copyright (c)  EMMA development team\n'
        'This program comes with NO WARRANTY.\n'
        'This is free software, and you are welcome to use and redistribute it\n'
        'under the conditions as specified in the license; see LICENSE\n'
    )


@app_emma.command(name='run', help='execution of EMMA with customisation of the basic optional arguments')
def run(
        map_files: te.Annotated[typing.List[str], typer.Argument(help='hydrodynamic output map-file(s)')],
        export: te.Annotated[bool, typer.Option(help='export model data to [wd]')] = True,
        f_eco_config: te.Annotated[str, typer.Option(help='ecotope configuration file')] = 'emma.json',
        f_map_config: te.Annotated[str, typer.Option(help='map configuration file')] = 'dfm1.json',
        log: te.Annotated[str, typer.Option(callback=__log_levels, help='level of log statements')] = 'WARNING',
        n_cores: te.Annotated[int, typer.Option(min=1, help='number of cores for parallel computations')] = 1,
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


@app_emma.command(name='compare', help='[NOT YET IMPLEMENTED] compare EMMA predictions to existing ecotope-maps')
def compare(
        map_files: te.Annotated[typing.List[str], typer.Argument(help='hydrodynamic output map-file(s)')],
        f_ecotopes: te.Annotated[str, typer.Argument(help='file with ecotope polygon data')],
        wd: te.Annotated[str, typer.Option(help='working directory')] = None,
) -> None:
    """Compare predictions of ecotopes based on EMMA with existing polygon-data of ecotopes.

    :param map_files: file name(s) of hydrodynamic model output data (*.nc)
    :param f_ecotopes: file name of ecotope-polygon data
    :param wd: working directory, defaults to None

    :type map_files: list[str]
    :type f_ecotopes: str
    :type wd: str, optional
    """
    __print_statements()
    print(
        f'The compare function is not yet implemented.\n'
    )
    sys.exit(1)


if __name__ == '__main__':
    # Execute the EMMA-application.
    app_emma()
