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
    classify_class_public_attrs,
)

from genuuml.tests.demo import (
    Foo, Baa, Baz, Mixin, MixinFoo,
)


class TestResolveTypes:
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


class TestClassifyClassAttrs:
    def test_with_object(self):
        attrs = classify_class_public_attrs(object)
        assert attrs == []

    def test_with_Foo(self):
        attrs = classify_class_public_attrs(Foo)
        for name, kind, value in attrs:
            print(name, kind)

        assert len(attrs) == 8
        expects = {
            '__init__': 'method',
            'STATIC_METHOD_FOO': 'static method',
            'CLASS_METHOD_FOO': 'class method',
            'object_method_foo': 'method',
            'property_foo': 'data descriptor',
            'property_get_foo': 'method',
            'property_set_foo': 'method',
            'CLASS_PROP_FOO': 'data',
        }
        for name, kind, value in attrs:
            assert kind == expects[name]


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
        assert obj.class_methods == []
        assert obj.static_methods == []
        assert obj.properties == []
        assert obj.methods == []
        assert obj.data_descriptors == []
        assert obj.data == []

    def test_inspect_with_Baz(self):
        obj = self.registry.inspect(Baz)

        assert type(obj.klass) == type
        assert type(obj.module) == ModuleType
        assert obj.module_path == 'genuuml.tests.demo'
        assert obj.class_path == 'genuuml.tests.demo.Baz'
        assert obj.file_path == locate(Baz.__module__).__file__
        assert set(obj.parents) == set([self.registry.get('genuuml.tests.demo.Baa')])
        assert obj.class_methods == ['CLASS_METHOD_BAZ']
        assert obj.static_methods == ['STATIC_METHOD_BAZ']
        assert obj.properties == []
        assert set(obj.methods) == set(['__init__', 'object_method_baz', 'get_baz', 'set_baz'])
        assert obj.data_descriptors == ['baz']
        assert obj.data == ['CLASS_PROP_BAZ']
