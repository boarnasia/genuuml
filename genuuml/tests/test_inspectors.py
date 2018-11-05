"""
Tests for genuuml.inspectors module
"""

from types import (
    ModuleType,
)
from pydoc import locate

import pytest

from genuuml.inspectors import (
    ClassNotFoundError,
    resolve_type,
    ClassRegistry,
    ClassInspector,
)

from genuuml.tests.demo import (
    Foo, Baa, Baz, Mixin, MixinFoo,
)


class TestResolveTypes:
    """
    Test resolve_type, resolve_type_from_instance and resolve_type_from_string.
    """

    def test_resolve_type_from_type(self):
        # Basic instance test
        t = resolve_type(Foo)
        assert type(t) == type

        # Builtin instance test
        t = resolve_type(object)
        assert type(t) == type

    def test_resolve_type_from_instance(self):
        # Basic instance test
        obj = Foo(1, 1)
        t = resolve_type(obj)
        assert type(t) == type

        # Builtin instance test
        obj = object()
        t = resolve_type(obj)
        assert type(t) == type

        # NoneType instance test
        obj = type(None)()
        t = resolve_type(obj)
        assert type(t) == type

    def test_resolve_type_from_string(self):
        # Basic class test
        t = resolve_type('genuuml.tests.demo.Foo')
        assert type(t) == type

        # Builtin class test 1
        t = resolve_type('object')
        assert type(t) == type

        # Builtin class test 2
        t = resolve_type('str')
        assert type(t) == type

        # No defined class test
        with pytest.raises(ClassNotFoundError):
            t = resolve_type('aaaa')


class TestClassRegistry:

    def setup_method(self):
        self.registry = ClassRegistry()


    def test_inspect(self):
        a = self.registry.inspect(Foo)
        b = self.registry.inspect(Foo)

        assert id(a) == id(b)


class TestClassInspector:

    def setup_method(self):
        self.registry = ClassRegistry()

    def test_inspect_with_object(self):
        obj = self.registry.inspect(object)

        assert type(obj.klass) == type
        assert type(obj.module) == ModuleType
        assert obj.module_path == 'builtins'
        assert obj.class_path == 'builtins.object'
        assert obj.file_path == ''
        assert obj.parents == []
        assert obj.full_public_properties == []
        assert obj.full_public_methods == []

        # Fixme: how do i know properties are automatically added?
        # assert obj.full_properties == ['__doc__']
        # assert obj.full_private_properties == ['__doc__']
        # assert obj.full_methods == [
        #     '__class__', '__delattr__', '__dir__', '__eq__', '__format__',
        #     '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
        #     '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__',
        #     '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        #     '__sizeof__', '__str__', '__subclasshook__',]
        # assert obj.full_private_methods == [
        #     '__class__', '__delattr__', '__dir__', '__eq__', '__format__',
        #     '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
        #     '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__',
        #     '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        #     '__sizeof__', '__str__', '__subclasshook__',]

        # Fixme: how do i distincts properties b/w local and inherited
        # obj.properties                # local properties
        # obj.private_properties
        # obj.public_properties
        # obj.methods                   # local methods
        # obj.private_methods
        # obj.public_methods

    def test_inspect_with_Baz(self):
        obj = self.registry.inspect(Baz)

        assert type(obj.klass) == type
        assert type(obj.module) == ModuleType
        assert obj.module_path == 'genuuml.tests.demo'
        assert obj.class_path == 'genuuml.tests.demo.Baz'
        assert obj.file_path == locate(Baz.__module__).__file__
        assert set(obj.parents) == set([self.registry.get('genuuml.tests.demo.Baa')])
#         # Fixme: how do i know properties are automatically added?
#         # assert obj.full_properties == [
#         #     '__doc__',
#         #     'CLASS_PROP_FOO',
#         #     'CLASS_PROP_BAA',
#         #     'CLASS_PROP_BAZ',
#         # ]
#         # assert obj.full_private_properties == ['__doc__']
#         assert set(obj.full_public_properties) == set([
#             'CLASS_PROP_FOO',
#             'CLASS_PROP_BAA',
#             'CLASS_PROP_BAZ',
#         ])
#         # Fixme: how do i know properties are automatically added?
#         # assert obj.full_methods == [
#         #     '__class__', '__delattr__', '__dir__', '__eq__', '__format__',
#         #     '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
#         #     '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__',
#         #     '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
#         #     '__sizeof__', '__str__', '__subclasshook__',
#         #     'CLASS_METHOD_FOO', 'CLASS_METHOD_BAA', 'CLASS_METHOD_BAZ',
#         #     'objec_method_foo', 'objec_method_baa', 'objec_method_baz',
#         # ]
#         # assert obj.full_private_methods == [
#         #     '__class__', '__delattr__', '__dir__', '__eq__', '__format__',
#         #     '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
#         #     '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__',
#         #     '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
#         #     '__sizeof__', '__str__', '__subclasshook__',]
#         assert set(obj.full_public_methods) == set([
#             'CLASS_METHOD_FOO', 'CLASS_METHOD_BAA', 'CLASS_METHOD_BAZ',
#             'object_method_foo', 'object_method_baa', 'object_method_baz',
#         ])
# 
# 
