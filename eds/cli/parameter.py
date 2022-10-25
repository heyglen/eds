import functools
import logging
from dataclasses import dataclass
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

        with Session() as session_:
            return fn(
                session=session_,
                *args,
                **kwargs,
            )

    return functools.update_wrapper(session_decorator, fn)


@dataclass
class _Argument:
    active: Callable = click.argument("active")
    session: Callable = session
    authentication_domain: Callable = click.argument("authentication-domain")
    checksum: Callable = click.argument("checksum")
    command: Callable = click.argument("command")
    destination: Callable = click.argument("destination", type=click.Path(exists=True))
    domain: Callable = click.argument("domain")
    file: Callable = click.argument(
        "file", type=click.Path(exists=True, dir_okay=False, readable=True)
    )
    script: Callable = click.argument(
        "script", type=click.Path(exists=True, dir_okay=False, readable=True)
    )
    file_name: Callable = click.argument("file-name")
    host: Callable = click.argument("host")
    hostname: Callable = click.argument("hostname")
    hostnames: Callable = click.argument("hostnames", nargs=-1)
    ip: Callable = click.argument("ip")
    name: Callable = click.argument("name")
    password: Callable = click.argument("password")
    port: Callable = click.argument("port")
    source: Callable = click.argument("source", type=click.Path(exists=True))
    software: Callable = click.argument("software", type=click.Path())
    standby: Callable = click.argument("standby")
    sha512_checksum: Callable = click.argument("sha512-checksum")
    user: Callable = click.argument("user")
    username: Callable = click.argument("username")


argument = _Argument()


@dataclass
class _Option:
    debug: Callable = click.option("-d", "--debug", help="Debug", count=True)
    domain: Callable = click.option(
        "--domain",
        default="ad.noc.nnit.com",
        show_default=True,
        help="Authentication domain",
    )
    repeat: Callable = click.option("--repeat", type=int)
    vrf: Callable = click.option("--vrf")
    interface: Callable = click.option("--interface")
    drive: Callable = click.option("--drive", default="flash", show_default=True)
    with_hostname: Callable = click.option(
        "--with-hostname",
        is_flag=True,
        default=False,
        help="Print the hostname with the output",
    )
    verbose: Callable = click.option("-v", "--verbose", is_flag=True, default=False)
    password: Callable = click.option("--password", is_flag=True, default=False)
    version: Callable = click.option("-V", "--version", is_flag=True, default=False)
    sha512_checksum: Callable = click.option("--sha512-checksum")
    username: Callable = click.option(
        "--username", help="Will default to the user in the users OpenSSH configuration"
    )


option = _Option()
