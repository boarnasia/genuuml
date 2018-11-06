"""
Genuuml Application module
"""

from typing import List
from importlib import import_module

import click

from .inspectors import ClassRegistry, ClassNotFoundError
from .builders import PlantUMLBuilder, AsciiTreeBuilder


def module_path_to_class_path(paths: List[str]) -> List[str]:
    """
    Helper function.

    If given path was a module path, convert the module path into the class
    paths defined in it.
    """
    class_paths = list()
    for path in paths:
        # loop all paths
        try:
            # Duck test
            # Given path can be imported by using `import_module`, it's a
            # module path.
            module = import_module(path)
            for member in dir(module):
                # check members
                klass = getattr(module, member)
                if type(klass) == type:
                    # Collect class path if the member is a class.
                    class_path = klass.__module__ + '.' + klass.__name__
                    class_paths.append(class_path)

        except ModuleNotFoundError:
            # Oops, the path isn't a module path.
            # That may be a class path.
            class_paths.append(path)

    return class_paths


def build_registry(class_paths: List[str]) -> List:
    """
    Helper function.
    Build and return ClassRegistry instance.

    :param class_paths: Class path list.
    :return: list consisting with ClassRegistry object and not found path list
    """
    class_paths = module_path_to_class_path(class_paths)
    registry = ClassRegistry()
    not_founds = []
    for path in class_paths:
        try:
            registry.inspect(path)
        except ClassNotFoundError as e:
            not_founds.append(e.args[1])

    return [registry, not_founds]


def in_plant_uml(class_paths: List[str]) -> List:
    """
    Return source in plant uml format by inspecting given class paths.

    :param class_paths: List of class paths and module paths
    :return: Source in plant uml format and not found path list
    """
    registry, not_founds = build_registry(class_paths)
    builder = PlantUMLBuilder(
        indent=2,
        print_self=False,
        print_default_value=False,
        print_typehint=False
    )
    source = builder.build(registry)

    return [source, not_founds]


def in_ascii_tree(class_paths: List[str]) -> List:
    """
    Return source in ascii tree format by inspecting given class paths.

    :param class_paths: List of class paths and module paths
    :return: Source in ascii tree format and not found path list
    """
    registry, not_founds = build_registry(class_paths)
    builder = AsciiTreeBuilder()
    source = builder.build(registry)

    return [source, not_founds]
