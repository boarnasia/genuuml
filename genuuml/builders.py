"""
Source builders
"""

import re
import textwrap
from inspect import signature
from operator import itemgetter
from typing import Callable, Set, Dict

from tree_format import format_tree

from .inspectors import ClassRegistry, ClassInspector


class Builder:

    def __init__(self, indent:int=2):
        self.indent = indent

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

        return textwrap.indent(line, (" " * self.indent * indent_level)) + "\n"

    @property
    def indent(self) -> int:
        """
        Hold indent width.
        """
        return self.__indent

    @indent.setter
    def indent(self, val: int):
        self.__indent = val


class PlantUMLBuilder(Builder):
    def __init__(self,
                 indent: int = 2,
                 print_typehint: bool = False,
                 print_default_value: bool = False,
                 print_full_arguments: bool = False,
                 max_arguments_width: int = 25,
                 print_builtins_members: bool = False,
                 pre_script: str = (
                         "@startuml\n"
                         "\n"
                         "hide empty members\n"
                         "\n"),
                 post_script: str = "@enduml\n"
                 ):
        super().__init__(indent)
        self.print_typehint = print_typehint
        self.print_default_value = print_default_value
        self.print_full_arguments = print_full_arguments
        self.max_arguments_width = max_arguments_width
        self.print_builtins_members = print_builtins_members
        self.pre_script = pre_script
        self.post_script = post_script

    @property
    def print_typehint(self) -> bool:
        """
        Switch for printing typehint
        """
        return self._print_typehint
    
    @print_typehint.setter
    def print_typehint(self, val: bool):
        self._print_typehint = val
    
    @property
    def print_default_value(self) -> bool:
        """
        Switch for printing default value of method's arguments
        """
        return self._print_default_value
    
    @print_default_value.setter
    def print_default_value(self, val: bool):
        self._print_default_value = val

    @property
    def print_full_arguments(self) -> bool:
        """
        Switch for printing full of method's arguments
        """
        return self._print_full_arguments
    
    @print_full_arguments.setter
    def print_full_arguments(self, val: bool):
        self._print_full_arguments = val

    @property
    def max_arguments_width(self) -> int:
        """
        Width of method's argument string
        """
        return self._max_arguments_width
    
    @max_arguments_width.setter
    def max_arguments_width(self, val: int):
        self._max_arguments_width = val

    @property
    def print_builtins_members(self) -> bool:
        """
        Switch for printing members of builtin classes.
        """
        return self._print_builtins_members
    
    @print_builtins_members.setter
    def print_builtins_members(self, val: bool):
        self._print_builtins_members = val

    @property
    def pre_script(self) -> str:
        """
        Script that is printed before class definisions.
        ex: @startuml
        """
        return self._pre_script
    
    @pre_script.setter
    def pre_script(self, val: str):
        self._pre_script = val

    @property
    def post_script(self) -> str:
        """
        Script that is printed after class definisions.
        ex: @enduml
        """
        return self._post_script
    
    @post_script.setter
    def post_script(self, val: str):
        self._post_script = val

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

