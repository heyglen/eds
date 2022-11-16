# pylint: disable=too-many-arguments,unused-argument

import textwrap
from typing import TYPE_CHECKING

import click
from eds.cli.parameter import argument
from eds.mo.period import RelativeCost

if TYPE_CHECKING:
    from eds.mo import Period

HELP_TEXT = "Power"


def click_format(period: "Period", time_only=False) -> str:
    if time_only:
        when = period.when.strftime("%H:%M")
    else:
        when = period.when.strftime("%Y.%m.%d %H:%M")
    cost = f"{period.price:3}"
    if period.relative_price == RelativeCost.cheap:
        cost = click.style(f"{period.price:3}", fg="green")
    elif period.relative_price == RelativeCost.expensive:
        cost = click.style(f"{period.price:3}", fg="red")
    return f"{when} {cost} {period.currency_unit}"


@click.command()
@argument.session
async def get(session):
    date_printed = set()
    for period in await session.get():
        when = period.when.strftime("%Y.%m.%d")
        if when not in date_printed:
            click.echo(when)
            date_printed.add(when)
        click.echo(textwrap.indent(click_format(period, time_only=True), prefix="\t"))
