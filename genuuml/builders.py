"""
Source builders
"""

import re
from inspect import signature
from typing import Callable

from .inspectors import ClassRegistry, ClassInspector


class Builder:
    def __init__(self, indent=2):
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

        return (self.indent * " ") + line + "\n"

    @property
    def pre_script(self):
        """
        Return the post script to be inserted before the source.
        """
        
        return ""

    @property
    def post_script(self):
        """
        Return the post script to be inserted after the source.
        """

        return ""

class PlantUMLBuilder(Builder):

    def __init__(self, indent=2, print_self=False,
                 print_typehint=False, print_default_value=False):
        super().__init__(indent)
        self.print_self = print_self
        self.print_typehint = print_typehint
        self.print_default_value = print_default_value

    @property
    def pre_script(self):
        return (
            "@startuml\n"
            "\n"
            "hide empty members\n"
            "\n")

    @property
    def post_script(self):
        return "@enduml\n"

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
            source = "({builtin})"

        if not self.print_self:
            source = re.sub(r'self\s*,\s*', '', source)

        # Fixme: 変数名に使える値でちゃんと切ったほうがいい
        if not self.print_typehint:
            source = re.sub(r'\s*:\s*[^.,)=]*', '', source)
            source = re.sub(r'\s*->\s*[^.,)=]*$', '', source)

        # Fixme: 変数名に使える値でちゃんと切ったほうがいい
        if not self.print_default_value:
            source = re.sub(r'\s*=\s*[^.,)]*', '', source)

        return source


    def _build_class(self, klass: ClassInspector) -> str:
        source = 'class {} as "{}"'.format(
            klass.class_path,
            klass.name,
        )
        source += '{\n'

        for member in klass.full_public_properties:
            source += self.line("+" + member, 1)

        source += "\n" if len(klass.full_public_properties) > 0 else ""

        for method in klass.full_public_methods:
            sig = method + self._build_signature(getattr(klass.klass, method))
            source += self.line("+" + sig, 1)

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

