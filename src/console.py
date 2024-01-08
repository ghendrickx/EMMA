"""
Run EMMA from the command-line.

Author: Gijs G. Hendrickx
"""
import typing

import typer
import typing_extensions as te

from src import processing

APP = typer.Typer()


def __log_levels(log: str) -> str:
    # capitalise all strings
    log = log.upper()
    levels = 'DEBUG', 'INFO', 'WARNING', 'CRITICAL'

    # verify validity of `log`-argument
    if log not in levels:
        msg = f'Unknown log-level, {log}; choose one of {levels}'
        raise typer.BadParameter(msg)

    # return log-level
    return log


@APP.command(name='run', help='execution of EMMA with customisation of the basic optional arguments')
def run(
        map_files: te.Annotated[typing.List[str], typer.Argument(help='hydrodynamic output map-file(s)')],
        export: te.Annotated[bool, typer.Option(help='export model data to [wd]')] = True,
        f_eco_config: te.Annotated[str, typer.Option(help='ecotope configuration file')] = 'emma.json',
        f_map_config: te.Annotated[str, typer.Option(help='map configuration file')] = 'dfm1.json',
        log: te.Annotated[str, typer.Option(callback=__log_levels, help='level of log statements')] = 'WARNING',
        n_cores: te.Annotated[int, typer.Option(min=1, help='number of cores for parallel computations')] = 1,
        wd: te.Annotated[str, typer.Option(help='working directory')] = None,
) -> None:
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


@APP.command(name='compare', help='compare EMMA predictions to existing ecotope-maps')
def compare(
        map_files: te.Annotated[typing.List[str], typer.Argument(help='hydrodynamic output map-file(s)')],
        f_ecotopes: te.Annotated[str, typer.Argument(help='file with ecotope polygon data')],
) -> None:
    msg = f'The compare function is not yet implemented (map_files={map_files}, f_ecotopes={f_ecotopes})'
    raise NotImplementedError(msg)


if __name__ == '__main__':
    APP()
