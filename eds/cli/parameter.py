import asyncio
import functools
import logging
import platform
from typing import Callable

import click
import colorlog
from eds import Session, constant

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-2s%(reset)s %(asctime)s %(white)s%(message)s",
    datefmt=constant.LOG_DATE_FORMAT,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
    style="%",
)


def session(fn):
    @option.debug
    def session_decorator(*args, **kwargs):
        debug = kwargs.pop("debug", None)
        if debug:
            logger = logging.getLogger("eds")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        async def _run_in_session():
            async with Session() as session_:
                return await fn(
                    session=session_,
                    *args,
                    **kwargs,
                )

        # https://bugs.python.org/issue39232
        if platform.platform().lower().startswith("windows"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        return asyncio.run(_run_in_session())

    return functools.update_wrapper(session_decorator, fn)


class _Argument:
    def __init__(self):
        self.session: Callable = session


argument = _Argument()


class _Option:
    def __init__(self):
        self.debug: Callable = click.option("-d", "--debug", help="Debug", count=True)
        self.verbose: Callable = click.option(
            "-v", "--verbose", is_flag=True, default=False
        )
        self.version: Callable = click.option(
            "-V", "--version", is_flag=True, default=False
        )


option = _Option()
