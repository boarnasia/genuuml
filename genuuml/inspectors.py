"""
Inspectors
"""

import abc
import inspect
import re
from types import ModuleType
from importlib import import_module
from pydoc import locate, classify_class_attrs
from typing import List, Union


class ClassNotFoundError(ImportError):
    pass


def resolve_type(klass: Union[type, object, str]) -> type:
    """
    Return a type instance.

    This function accepts type, object and class path as an argument `klass`.
    If `klass` is a type instance, return it as is.
    If `klass` is a object, return the type instance of the object.
    If `klass` is a class path, return the type instance of the class path.

    Eventually, if type instance not be found, raise `ClassNotFoundError`.

    :param klass: Type instance, object or class path.
    :return: Type instance of `klass`
    """
    resolved_class = klass.__class__
    if type(klass) in [type, abc.ABCMeta]:
        resolved_class = klass

    elif type(klass) == str:
        resolved_class = locate(klass)

    if not type(resolved_class) in [type, abc.ABCMeta]:
        raise ClassNotFoundError("Class not found. [{}]".format(klass),
                                 klass)

    return resolved_class


def visiblename(name, all=None, obj=None) -> bool:
    """
    Decide whether to show documentation on a variable.
    Copied from `pydoc.visiblename`, difference is it return 0 when obj is
    `object` and name is those:

        __annotations__
        __dict__
        __weakref__
    """
    # Certain special names are redundant or internal.
    # XXX Remove __initializing__?
    if name in {'__author__', '__builtins__', '__cached__', '__credits__',
                '__date__', '__doc__', '__file__', '__spec__',
                '__loader__', '__module__', '__name__', '__package__',
                '__path__', '__qualname__', '__slots__', '__version__',
                '__annotations__', '__dict__', '__weakref__', }:
        return False
    # Private names are hidden, but special names are displayed.
    if name.startswith('__') and name.endswith('__'): return 1
    # Namedtuples have public fields and methods with a single leading underscore
    if name.startswith('_') and hasattr(obj, '_fields'):
        return True
    if all is not None:
        # only document that which the programmer exported in __all__
        return name in all
    else:
        return not name.startswith('_')


def classify_class_public_attrs(klass) -> List:
    """
    Return public attributes of given `klass`.
    It uses `pydoc.classify_class_attrs`.

    kind:
        'class method'    created via classmethod()
        'static method'   created via staticmethod()
        'property'        created via property()
        'method'          any other flavor of method or descriptor
        'data descriptor' data descriptor
        'data'            not a method

    Fixme: It may not collect properties correctly.

    :param klass: Class object
    :return: List of attributes consisting with name, kind and value
    """
    attrs = [(name, kind, value)
            for name, kind, cls, value in classify_class_attrs(klass)
            if visiblename(name, obj=klass) and cls==klass]

    return attrs

class ClassInspector:

    @property
    def klass(self) -> type:
        """
        Class object of target class
        """
        return self._klass

    @property
    def name(self):
        return self.klass.__name__

    @property
    def registry(self) -> 'ClassRegistry':
        """
        ClassRegistry object
        """
        return self._registry

    @property
    def module(self) -> ModuleType:
        """
        Module instance of target class
        """
        return self._module

    @property
    def module_path(self) -> str:
        return self.klass.__module__

    @property
    def class_path(self) -> str:
        return self.module_path + "." + self.name

    @property
    def file_path(self) -> str:
        return getattr(self.module, '__file__', "")

    @property
    def class_methods(self) -> List[str]:
        return self._class_methods

    @property
    def static_methods(self) -> List[str]:
        return self._static_methods

    @property
    def properties(self) -> List[str]:
        return self._properties

    @property
    def methods(self) -> List[str]:
        return self._methods

    @property
    def data_descriptors(self) -> List[str]:
        return self._data_descriptors

    @property
    def data(self) -> List[str]:
        return self._data

    @property
    def parents(self) -> List['ClassInspector']:
        return self._parents

    def __init__(self, klass: Union[type, object, str],
                 registry: 'ClassRegistry'):
        self._klass = resolve_type(klass)
        self._registry = registry
        self._module = locate(self.klass.__module__)

        self._class_methods = []
        self._static_methods = []
        self._properties = []
        self._methods = []
        self._data_descriptors = []
        self._data = []

        self._parents = []

        for parent in self.klass.__bases__:
            self.parents.append(self.registry.inspect(parent))

        attrs = classify_class_public_attrs(self.klass)

        for name, kind, value in attrs:
            if kind == 'class method':
                self.class_methods.append(name)
            elif kind == 'static method':
                self.static_methods.append(name)
            elif kind == 'property':
                self.properties.append(name)
            elif kind == 'method':
                self.methods.append(name)
            elif kind == 'data descriptor':
                self.data_descriptors.append(name)
            elif kind == 'data':
                self.data.append(name)
        self.class_methods.sort()
        self.static_methods.sort()
        self.properties.sort()
        self.methods.sort()
        self.data_descriptors.sort()
        self.data.sort()


    def __str__(self) -> str:
        return self.class_path if self.class_path else "(empty)"

    def __eq__(self, other: 'ClassInspector') -> bool:
        return hash(self) == hash(other)

    def __ne__(self, other: 'ClassInspector') -> bool:
        return not self.class_path == other.class_path

    def __hash__(self):
        return hash(self.class_path)


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

