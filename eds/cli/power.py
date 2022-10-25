# pylint: disable=too-many-arguments,unused-argument

import textwrap

import click
from eds.cli.parameter import argument

HELP_TEXT = "Power"


@click.command()
@argument.session
def get(session):
    date_printed = set()
    for period in session.get():
        when = period.when.strftime("%Y.%m.%d")
        if when not in date_printed:
            click.echo(when)
            date_printed.add(when)
        click.echo(textwrap.indent(period.click_format(time_only=True), prefix="\t"))
