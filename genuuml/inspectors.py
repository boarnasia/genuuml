"""
Inspectors
"""

import re
import types
from typing import List, Union
from importlib import import_module
import inspect
from pydoc import locate


class ClassNotFoundError(RuntimeError):
    pass


def resolve_type(klass: Union[type, object, str]) -> type:
    if type(klass) == type:
        return klass

    elif type(klass) == str:
        return locate(klass)

    return klass.__class__


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


class OldClassInspector():
    """
    Inspector for class
    """
    def __init__(self, class_path=None, class_object=None, instance=None):
        self.class_object = None
        if class_path:
            self.from_class_path(class_path)
        elif class_object:
            self.from_class_object(class_object)
        elif instance:
            self.from_instance(instance)

    def from_instance(self, instance):
        self.class_object = instance.__class__
        self._inspect_class_object()
        return self

    def from_class_object(self, class_object):
        self.class_object = class_object
        self._inspect_class_object()
        return self

    def from_class_path(self, class_path):
        path_list = class_path.split('.')
        target_class_name = path_list[-1]
        target_module_name = '.'.join(path_list[:-1])

        try:
            target_module = import_module(target_module_name)
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError("Module not found from path: " + class_path)

        try:
            self.class_object = getattr(target_module, target_class_name)
        except Attribute as e:
            raise ClassNotFoundError("Class not found from path: " + class_path)

        self._inspect_class_object()

        return self

    def has_bases(self):
        return len(self.bases) > 0

    def _inspect_class_object(self):
        self._inspect_module_structure()
        self._inspect_members()
        self._inspect_bases()

        return self

    def _inspect_module_structure(self):
        self.module_object = inspect.getmodule(self.class_object)
        self.class_name = self.class_object.__name__
        self.absolute_module_path = self.module_object.__name__
        self.absolute_class_path = self.absolute_module_path + '.' + self.class_name

    def _inspect_members(self):
        def get_signature(class_object, method_name):
            method_object = getattr(class_object, method_name)
            sigstr = method_name + str(inspect.signature(method_object))
            sigstr = re.sub(r"=<object[^>]*>", "=<object>", sigstr)
            return sigstr

        other_members = [ member for member in dir(self.class_object) if re.match(r'^__', member) ]
        members = [ attr for attr in dir(self.class_object) if attr not in other_members ]
        private_members = [ member for member in members if re.match(r'^_', member) ]
        public_members = [ member for member in members if re.match(r'^[^_]', member) ]
        self.public_methods_without_signature = [
            member for member in ['__init__'] + public_members
                    if type(getattr(self.class_object, member)) in
                            [types.FunctionType, types.MethodType]
        ]
        self.public_methods = [
            get_signature(self.class_object, member) for member in self.public_methods_without_signature
        ]
        self.public_properties = [ member for member in public_members
                                      if member not in self.public_methods_without_signature]
        self.private_methods_without_signature = [
            member for member in private_members
                    if type(getattr(self.class_object, member)) in
                            [types.FunctionType, types.MethodType]
        ]
        self.private_methods = [
            get_signature(self.class_object, member) for member in self.private_methods_without_signature
        ]
        self.private_properties = [ member for member in private_members
                                  if member not in self.private_methods_without_signature]

    def _inspect_bases(self):
        self.bases = []
        for class_object in self.class_object.__bases__:
            self.bases.append(ClassInspector(class_object=class_object))

    def __str__(self):
        return self.absolute_class_path

