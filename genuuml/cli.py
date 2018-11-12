from typing import List
from textwrap import indent

import click

from . import __version__
from . import genuuml


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
    PlantUML generator from python script

    Subcommands can be invoked by giving correct name or a partial name included in command name.

    Example:

    \b
        `in-plnat-uml` Correct command name is OK
        `in-ascii-tree` Correct command name is OK
        `in-p` A part of command name is also OK
        `in-` A part of command name matching more than one command is NG

    All subcommands receive CLASS_PATHS arguments.  CLASS_PATHS can be accepted that are class or module path, and those can be mixed.  When module path was given, it would be replaced into class paths defined in the module.
    """
    # Placeholder for subcommands
    pass


def _print_not_founds(not_founds: List[str]):
    if not_founds:
        click.secho("Given class not found.", fg='red', err=True)
        for class_path in not_founds:
            msg = indent("- " + class_path, "  ")
            click.secho(msg, fg='red', err=True)
        click.secho("=" * 60, fg='red', err=True)
        click.echo("")


@main.command()
@click.argument('class_paths', nargs=-1, required=True)
@click.option('-i', '--indent', default=2, type=int, help="Set indent level")
@click.option('--print-typehint/--no-print-typehint', default=False, help="Toggle typehint on/off")
@click.option('--print-default-value/--no-print-default-value', default=False, help="Toggle default value in method's arguments on/off")
@click.option('--print-full-arguments/--no-print-full-arguments', default=False, help="Toggle full method's arguments on/off")
@click.option('--max-arguments-width', default=25, type=int, help="Method's arguments width")
@click.option('--print-builtins-members/--no-print-builtins-members', default=False, help="Toggle print members of builtin classes on/off")
def in_plant_uml(class_paths, indent, print_typehint, print_default_value,
                 print_full_arguments, max_arguments_width, print_builtins_members):
    """
    Print in PlantUML format.
    """
    source, not_founds = genuuml.in_plant_uml(class_paths, indent,
                                              print_typehint, print_default_value,
                                              print_full_arguments, max_arguments_width,
                                              print_builtins_members
                                              )

    _print_not_founds(not_founds)

    click.echo(source)


@main.command()
@click.argument('class_paths', nargs=-1, required=True)
def in_ascii_tree(class_paths):
    """
    Print in Ascii Tree format.
    """
    source, not_founds = genuuml.in_ascii_tree(class_paths)

    _print_not_founds(not_founds)

    click.echo(source)


@main.command()
@click.argument('class_paths', nargs=-1, required=True)
def in_filepath_list(class_paths):
    """
    Print in Filepath list format.
    """
    source, not_founds = genuuml.in_filepath_list(class_paths)

    _print_not_founds(not_founds)

    click.echo(source)


if __name__=='__main__':
    main()
