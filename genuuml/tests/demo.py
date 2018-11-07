"""
Demonstlation classes for test.

Structure is:

object
  +- Foo
    +- Baa
      +- Baz
    + MixinFoo
  + Mixin
    + MixinFoo

In reverse:

Baz
  +- Baa
    +- Foo

MixinFoo
  +- Foo
    +- object
  +- Mixin
    +- object
"""

class Foo(object):
    CLASS_PROP_FOO: bool = True

    def __init__(self, arg: list, kwarg: dict=True):
        self.object_prop_foo: bool = True

    @staticmethod
    def STATIC_METHOD_FOO(arg: list, kwarg: dict=True) -> str:
        pass

    @classmethod
    def CLASS_METHOD_FOO(cls, arg: list, kwarg: dict=True) -> str:
        pass

    def object_method_foo(self, arg: list, kwarg: dict=True) -> str:
        pass

    def property_get_foo(self):
        pass

    def property_set_foo(self):
        pass

    property_foo = property(property_get_foo, property_set_foo)


class Baa(Foo):
    CLASS_PROP_BAA: bool = True

    def __init__(self, arg: list, kwarg: list=True):
        self.object_prop_baa: bool = True

    @classmethod
    def CLASS_METHOD_BAA(cls, arg: list, kwarg: dict=True) -> str:
        pass

    def object_method_baa(self, arg: list, kwarg: dict=True) -> str:
        pass

class Baz(Baa):
    CLASS_PROP_BAZ: bool = True

    def __init__(self, arg: list, kwarg: dict=True):
        self.object_prop_baz: bool = True

    @staticmethod
    def STATIC_METHOD_BAZ(arg: list, kwarg: dict=True) -> str:
        pass

    @classmethod
    def CLASS_METHOD_BAZ(cls, arg: list, kwarg: dict=True) -> str:
        pass

    def object_method_baz(self, arg: list, kwarg: dict=True) -> str:
        pass

    def get_baz(self, arg: list, kwarg: dict=True) -> str:
        pass

    def set_baz(self, arg: list, kwarg: dict=True) -> str:
        pass

    baz = property(get_baz, set_baz)


class Mixin(object):
    CLASS_PROP_MIXIN: bool = True

    def __init__(self, arg: list, kwarg: dict=True):
        self.object_prop_mixin: bool = True

    @classmethod
    def CLASS_METHOD_MIXIN(cls, arg: list, kwarg: dict=True) -> str:
        pass

    def object_method_mixin(self, arg: list, kwarg: dict=True) -> str:
        pass

class MixinFoo(Mixin, Foo):
    CLASS_PROP_MIXINFOO: bool = True

    def __init__(self, arg: list, kwarg: dict=True):
        self.object_prop_mixinfoo: bool = True

    @classmethod
    def CLASS_METHOD_MIXINFOO(cls, arg: list, kwarg: dict=True) -> str:
        pass

    def object_method_mixinfoo(self, arg: list, kwarg: dict=True) -> str:
        pass
