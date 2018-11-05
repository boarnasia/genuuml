import sys
from typing import List
from importlib import import_module

import click

from .utils import exit
# from .inspectors import OldClassInspector
# from .printers import PlantUMLPrinter
from .inspectors import ClassRegistry, ClassNotFoundError
from .builders import PlantUMLBuilder, AsciiTreeBuilder
from . import __version__


def _module_to_class(paths: List[str]) -> List[str]:
    """
    Helper function.
    """
    ret = list()
    for path in paths:
        try:
            module = import_module(path)
            for member in dir(module):
                klass = getattr(module, member)
                if type(klass) == type:
                    class_path = klass.__module__ + '.' + klass.__name__
                    ret.append(class_path)
        except ModuleNotFoundError:
            ret.append(path)

    return ret


def _build_registry(class_paths: List[str]) -> ClassRegistry:
    """
    Helper function.
    Build and return ClassRegistry instance.

    :param class_paths: Class path list.
    """
    class_paths = _module_to_class(class_paths)
    registry = ClassRegistry()
    try:
        for path in class_paths:
            registry.inspect(path)
    except ClassNotFoundError as e:
        click.secho('Given class [{}] not found.'.format(e.args[1]),
                    fg='red',
                    err=True)
        sys.exit(1)

    return registry



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
    Print given classes information in PlantUML format or Ascii Tree format.

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


@main.command()
@click.argument('class_paths', nargs=-1, required=True)
def in_plant_uml(class_paths):
    """
    Print in PlantUML format.
    """
    registry = _build_registry(class_paths)
    builder = PlantUMLBuilder(
        indent=2,
        print_self=False,
        print_default_value=False,
        print_typehint=False
    )
    source = builder.build(registry)
    click.echo(source)


@main.command()
@click.argument('class_paths', nargs=-1, required=True)
def in_ascii_tree(class_paths):
    """
    Print in Ascii Tree format.
    """
    registry = _build_registry(class_paths)
    builder = AsciiTreeBuilder()
    source = builder.build(registry)
    click.echo(source)


if __name__=='__main__':
    main()
