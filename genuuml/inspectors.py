"""
Inspectors
"""

import re
import types
from typing import List, Union
from importlib import import_module
import inspect
from pydoc import locate


class ClassNotFoundError(ImportError):
    pass


def resolve_type(klass: Union[type, object, str]) -> type:
    resolved_class = klass.__class__
    if type(klass) == type:
        resolved_class = klass

    elif type(klass) == str:
        resolved_class = locate(klass)

    if not type(resolved_class) == type:
        raise ClassNotFoundError("Class not found. [{}]".format(klass))

    return resolved_class


class ClassInspector:
    def __init__(self, klass: Union[type, object, str],
                 registry: 'ClassRegistry'):
        self.registry = registry

        self.klass = None
        self.module = None
        self.module_path = ""
        self.class_path = ""
        self.file_path = ""

        # self.properties = []
        # self.private_properties = []
        # self.public_properties = []
        self.full_properties = []
        self.full_private_properties = []
        self.full_public_properties = []

        # self.methods = []
        # self.private_methods = []
        # self.public_methods = []
        self.full_methods = []
        self.full_private_methods = []
        self.full_public_methods = []

        self.parents: list[ClassInspector] = []

        self._inspect(klass)


    def _inspect(self, klass: Union[type, object, str]):
        self.klass = resolve_type(klass)
        self.name = self.klass.__name__
        self.module_path = self.klass.__module__
        self.module = locate(self.klass.__module__)
        self.class_path = self.module_path + "." + self.name
        self.file_path = getattr(self.module, '__file__', "")

        for parent in self.klass.__bases__:
            self.parents.append(self.registry.inspect(parent))

        for attr in dir(self.klass):
            if callable(getattr(self.klass, attr)):
                self.full_methods.append(attr)
            else:
                self.full_properties.append(attr)

        for prop in self.full_properties:
            if re.match(r'^_', prop):
                self.full_private_properties.append(prop)
            else:
                self.full_public_properties.append(prop)

        for method in self.full_methods:
            if re.match(r'^_', method):
                self.full_private_methods.append(method)
            else:
                self.full_public_methods.append(method)

    def __str__(self) -> str:
        return self.class_path if self.class_path else "(empty)"

    def __eq__(self, other: 'ClassInspector') -> bool:
        return self.class_path == other.class_path

    def __ne__(self, other: 'ClassInspector') -> bool:
        return not self.class_path == other.class_path


class ClassRegistry(dict):

    def inspect(self, klass: Union[type, object, str]) -> ClassInspector:
        """
        return new inspected class or existing one if that's already in list.
        In addition, register all ancentors of the class given.
        """
        resolved_class = resolve_type(klass) 
        class_path = resolved_class.__module__ + '.' + resolved_class.__name__

        if self.get(class_path, None) is None:
            inspected_class = ClassInspector(resolved_class, self)
            self[class_path] = inspected_class

        return self.get(class_path)

