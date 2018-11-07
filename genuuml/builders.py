"""
Source builders
"""

import re
from inspect import signature
from typing import Callable, Set, Dict
from operator import itemgetter

from tree_format import format_tree

from .inspectors import ClassRegistry, ClassInspector


class Builder:
    indent: int = 2
    pre_script: str = ""
    post_script: str = ""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def build(self, registry: ClassRegistry) -> str:
        """
        Build the source and return.
        Please use after implementation.

        :param registry: ClassRegistry object to be built.
        """
        raise NotImplementedError("Call after implemented")

    def line(self, line: str, indent_level:int =0):
        """
        Return a line concated with indent, given line and linebreak.

        :param line: string to be a line in source
        :param indnet_level: indent level of the line
        """

        return (self.indent * " ") + line + "\n"


class PlantUMLBuilder(Builder):
    print_typehint: bool = False
    print_default_value: bool = False
    print_full_arguments: bool = False
    max_arguments_width: int = 25
    print_builtins_members: bool = False
    pre_script: str = (
            "@startuml\n"
            "\n"
            "hide empty members\n"
            "\n")
    post_script: str = "@enduml\n"

    def build(self, registry: ClassRegistry) -> str:
        source = self.pre_script
        source += self._build_all_classes(registry)
        source += self._build_all_relations(registry)
        source += self.post_script

        return source

    def _build_signature(self, method: Callable) -> str:
        source = ""
        try:
            source = str(signature(method))
        except ValueError:
            source = "(...)"

        # Fixme: 変数名に使える値でちゃんと切ったほうがいい
        if not self.print_typehint:
            source = re.sub(r'\s*:\s*[^,)=]*', '', source)
            source = re.sub(r'\s*->\s*[^,)=]*$', '', source)

        # Fixme: 変数名に使える値でちゃんと切ったほうがいい
        if not self.print_default_value:
            source = re.sub(r'\s*=\s*[^.,)]*', '', source)

        if not self.print_full_arguments:
            mx = self.max_arguments_width
            source = (source[:mx] + ' ... )') if len(source) > mx else source

        return source


    def _build_class(self, klass: ClassInspector) -> str:
        source = 'class {} as "{}"'.format(
            klass.class_path,
            klass.name,
        )
        source += '{\n'

        if not klass.module_path == object.__module__ or self.print_builtins_members:
            props = klass.data + klass.data_descriptors + klass.properties
            methods = klass.static_methods + klass.class_methods + klass.methods
            props.sort()
            methods.sort()

            for member in props:
                line = "+" + member
                source += self.line(line, 1)

            static_like_methods = klass.static_methods + klass.class_methods
            for method in methods:
                line = "+" + method + self._build_signature(getattr(klass.klass, method))
                if method in static_like_methods:
                    line = "{static}" + line

                source += self.line(line, 1)

        source += "}\n\n"

        return source

    def _build_all_classes(self, registry: ClassRegistry) -> str:
        source = ""

        for class_path in registry.keys():
            klass = registry.get(class_path)
            source += self._build_class(klass)

        return source

    def _build_all_relations(self, registry: ClassRegistry) -> str:
        source = ""

        for class_path in registry.keys():
            klass = registry.get(class_path)

            for parent in klass.parents:
                source += "{} -up-|> {}\n".format(
                    klass.class_path, parent.class_path)

        source += "\n"

        return source


class AsciiTreeBuilder(Builder):

    def build(self, registry: ClassRegistry) -> str:
        """
        Build the source and return.

        :param registry: ClassRegistry object to be built.
        """
        #import pudb; pu.db

        children = self._build_children(registry)
        tree = self._build_tree('builtins.object', children)
        source = format_tree(
            tree,
            format_node=itemgetter(0), 
            get_children=itemgetter(1)
        )

        return source

    def _build_children(self, registry: ClassRegistry) -> str:
        children = dict()
        for class_path_outer in registry.keys():
            klass: ClassInspector = registry[class_path_outer]
            for class_inner in klass.parents:
                class_path_inner = class_inner.class_path
                if not class_path_inner in children.keys():
                    children[class_path_inner] = list()
                children[class_path_inner].append(class_path_outer)
        return children
                

    def _build_tree(self, root: str, src: Dict) -> str:
        children = []
        for child in src.get(root, []):
            children.append(self._build_tree(child, src))
        return [root, children]

