import logging

import click
from eds.cli import power
from eds.cli.parameter import argument, option
from eds.eds import Eds

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(
    help_option_names=["-h"],
)


@click.group(
    invoke_without_command=True, context_settings=CONTEXT_SETTINGS, no_args_is_help=True
)
@option.version
def commands(version):
    if version:
        click.echo(Eds.version)


def build_group(name=None, help_=None, short_help=None, module=None):
    if name is None:
        if module is None:
            raise ValueError("A Group name or module must be specified")
        name = module.__name__.split(".")[-1].replace("_", "-")
    module = module or dict()
    group = click.Group(name)
    group.help = getattr(module, "HELP_TEXT", None) or help_ or ""
    group.short_help = (
        getattr(module, "SHORT_HELP_TEXT", None) or short_help or group.help or ""
    )
    return group


def group_attach_module_commands(module, group, parent_group):
    has_commands = False
    for cmd in dir(module):
        command = getattr(module, cmd)
        if isinstance(command, click.core.Command):
            group.add_command(command)
            has_commands = True
    if has_commands:
        parent_group.add_command(group)


normal_groups = [power]

for cli_module in normal_groups:
    group = build_group(module=cli_module)
    group_attach_module_commands(cli_module, group, commands)
