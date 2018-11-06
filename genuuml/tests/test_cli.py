"""
Tests for genuuml.cli module
"""

import pytest

from genuuml.cli import (
    _module_path_to_class_path,
    _build_registry,
)


def test_module_path_to_class_path():
    # Class path is not converted.
    ret = _module_path_to_class_path(['genuuml.tests.demo.Foo'])
    assert ret == ['genuuml.tests.demo.Foo']

    # Module path is converted into class paths.
    ret = _module_path_to_class_path(['genuuml.tests.demo'])
    assert set(ret) == set(['genuuml.tests.demo.Baa', 'genuuml.tests.demo.Baz', 'genuuml.tests.demo.Foo', 'genuuml.tests.demo.Mixin', 'genuuml.tests.demo.MixinFoo'])

    # Builtin classes leave it as is.
    ret = _module_path_to_class_path(['object'])
    assert set(ret) == set(['object'])

    # Also other than class path, module path and builtin classes leave it as is.
    ret = _module_path_to_class_path(['not_class_path'])
    assert set(ret) == set(['not_class_path'])

    # Mixture is acceptable.
    ret = _module_path_to_class_path(['genuuml.tests.demo', 'object'])
    assert set(ret) == set(['genuuml.tests.demo.Baa', 'genuuml.tests.demo.Baz', 'genuuml.tests.demo.Foo', 'genuuml.tests.demo.Mixin', 'genuuml.tests.demo.MixinFoo', 'object'])


def test_build_registry():
    # Usual class is OK.
    ret = _build_registry(['genuuml.tests.demo.Foo']).keys()
    assert set(ret) == set(['builtins.object', 'genuuml.tests.demo.Foo'])

    # Builtin class is also acceptable.
    ret = _build_registry(['object']).keys()
    assert set(ret) == set(['builtins.object'])

    # Wrong class path is ignore.
    ret = _build_registry(['wrong_class_path']).keys()
    assert set(ret) == set([])

