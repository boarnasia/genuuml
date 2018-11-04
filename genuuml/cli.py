import click
from typing import List

from .utils import exit
# from .inspectors import OldClassInspector
# from .printers import PlantUMLPrinter
from .inspectors import ClassRegistry
from .builders import PlantUMLBuilder
from . import __version__


class AliasedGroup(click.Group):
    """
    Provide alias functionality for subcommands.

    Subcommands can be invoked by giving correct name or a part of string included in command name.

    Example:

    - `as-plnat-uml` Correct command name is OK
    - `as-ascii-tree` Correct command name is OK
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
        cmd_list = self.list_commands(ctx)
        matches = self._collect_commands(cmd_name, cmd_list)

        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])

        # A part matching multiple is NG.
        ctx.fail('Too many matches: {}'.format(
            ', '.join(sorted(matches))
        ))

        return rv

    @classmethod
    def _collect_commands(cls, cmd_name: str, cmd_list: List) -> List:
        """
        Collect and return command list that `cmd_name` matching with `cmd_list`.
        >>> cmd_list = ['as-plant-uml', 'as-ascii-tree']
        >>> AliasedGroup._collect_commands('as-plant-uml', cmd_list)
        ['as-plant-uml']

        >>> AliasedGroup._collect_commands('uml', cmd_list)
        ['as-plant-uml']

        >>> AliasedGroup._collect_commands('as', cmd_list)
        ['as-plant-uml', 'as-ascii-tree']
        """

        def idx_filter(item):
            try:
                item.index(cmd_name)
                return True
            except ValueError as e:
                return False

        return list(filter(idx_filter, cmd_list))


@click.group(cls=AliasedGroup)
@click.version_option(version=__version__)
def main():
    """
    Print given class information in PlantUML format or Ascii Tree format.

    Subcommands can be invoked by giving correct name or a partial name included in command name.

    Example:

    \b
        `as-plnat-uml` Correct command name is OK
        `as-ascii-tree` Correct command name is OK
        `as-p` A part of command name is also OK
        `as-` A part of command name matching more than one command is NG
    """
    pass


@main.command()
@click.argument('class_path')
def as_plant_uml(class_path):
    """
    Print in PlantUML format.
    """
    click.echo(class_path)
    registry = ClassRegistry()
    try:
        registry.inspect(class_path)
    except ImportError as e:
        exit("Module or Class has not found. [{}]".format(target_class_path), exit_code=1)
    builder = PlantUMLBuilder(
        indent=2,
        print_self=False,
        print_default_value=False,
        print_typehint=False
    )
    source = builder.build(registry)
    click.echo(source)


@main.command()
@click.argument('class_path')
def as_ascii_tree(class_path):
    """
    Print in Ascii Tree format.
    """
    click.echo("Not implemented yet.")


if __name__=='__main__':
    main()
