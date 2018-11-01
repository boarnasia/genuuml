"""
Inspectors
"""

import re
import types
from importlib import import_module
import inspect


class ClassNotFoundError(ModuleNotFoundError):
    pass


class ClassInspector():
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
        self.module_object = inspect.getmodule(self.class_object)
        self.class_name = self.class_object.__name__
        self.absolute_module_path = self.module_object.__name__
        self.absolute_class_path = self.absolute_module_path + '.' + self.class_name

        def get_signature(class_object, method_name):
            method_object = getattr(class_object, method_name)
            sigstr = method_name + str(inspect.signature(method_object))
            sigstr = re.sub(r"=<object[^>]*>", "=<object>", sigstr)
            return sigstr

        other_members = [ member for member in dir(self.class_object) if re.match(r'^__', member) ]
        members = [ attr for attr in dir(self.class_object) if attr not in other_members ]
        private_members = [ member for member in members if re.match(r'^_', member) ]
        public_members = [ member for member in members if re.match(r'^[^_]', member) ]
        self.public_methods = [
            get_signature(self.class_object, member) for member in ['__init__'] + public_members
                    if type(getattr(self.class_object, member)) in
                            [types.FunctionType, types.MethodType]
        ]
        self.public_properties = [ member for member in public_members
                                      if member not in self.public_methods]
        self.private_methods = [
            get_signature(self.class_object, member) for member in private_members
                    if type(getattr(self.class_object, member)) in
                            [types.FunctionType, types.MethodType]
        ]
        self.private_properties = [ member for member in private_members
                                  if member not in self.private_methods]

        self.bases = []
        for class_object in self.class_object.__bases__:
            self.bases.append(ClassInspector(class_object=class_object))

        return self

    def __str__(self):
        return self.absolute_class_path

