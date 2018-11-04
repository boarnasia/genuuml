from os.path import join, dirname
from argparse import ArgumentParser

import click

from .utils import exit
from .inspectors import ClassInspector
from .printers import PlantUMLPrinter
from . import __version__


class AliasedGroup(click.Group):
    """
    Provide alias functionality for subcommands.

    Subcommands can be invoked by giving correct name or a part of string included in command name.

    Example:

    - `as-plnat-uml` Corrent command name is OK
    - `as-ascii-tree` Corrent command name is OK
    - `as-p` A part of command name is also OK
    - `as-` A part of command name matching more than one command is NG

    See https://pocoo-click.readthedocs.io/en/latest/advanced/#command-aliases
    """

    def get_command(self, ctx, cmd_name):
        # Correct name is OK
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # A part of command name is also OK
        commands = self.list_commands(ctx)
        matches = []
        for command in commands:
            try:
                command.index(cmd_name)
                matches.append(command)
            except ValueError:
                pass

        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])

        # A part matching multiple is NG.
        ctx.fail('Too many matches: {}'.format(
            ', '.join(sorted(matches))
        ))

        return rv


@click.group(cls=AliasedGroup)
@click.version_option(version=__version__)
def main():
    """
    Print given class information in PlantUML format or Ascii Tree format.

    Subcommands can be invoked by giving correct name or a partial name included in command name.

    Example:

    \b
        `as-plnat-uml` Corrent command name is OK
        `as-ascii-tree` Corrent command name is OK
        `as-p` A part of command name is also OK
        `as-` A part of command name matching more than one command is NG
    """
    pass
    # parser = _parse_args()
    # class_hierarchy = generate_class_hierarchy(parser.target_class)
    # printer = PlantUMLPrinter(class_hierarchy)
    # print(printer.source)


@main.command()
@click.argument('class_path')
def as_plant_uml(class_path):
    """
    Print in PlantUML format.
    """
    try:
        inspector = ClassInspector(class_path=class_path)
    except ImportError as e:
        exit("Module or Class has not found. [{}]".format(target_class_path), exit_code=1)
    printer = PlantUMLPrinter(inspector)
    click.echo(printer.source)


@main.command()
@click.argument('class_path')
def as_ascii_tree(class_path):
    """
    Print in Ascii Tree format.
    """
    click.echo("Not implemented yet.")


if __name__=='__main__':
    main()
