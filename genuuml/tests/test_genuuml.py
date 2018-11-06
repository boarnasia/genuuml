"""
Tests for genuuml.cli module
"""

import pytest

from genuuml.genuuml import (
    module_path_to_class_path,
    build_registry,
)


def test_module_path_to_class_path():
    # Class path is not converted.
    ret = module_path_to_class_path(['genuuml.tests.demo.Foo'])
    assert ret == ['genuuml.tests.demo.Foo']

    # Module path is converted into class paths.
    ret = module_path_to_class_path(['genuuml.tests.demo'])
    assert set(ret) == set(['genuuml.tests.demo.Baa', 'genuuml.tests.demo.Baz', 'genuuml.tests.demo.Foo', 'genuuml.tests.demo.Mixin', 'genuuml.tests.demo.MixinFoo'])

    # Builtin classes leave it as is.
    ret = module_path_to_class_path(['object'])
    assert set(ret) == set(['object'])

    # Also other than class path, module path and builtin classes leave it as is.
    ret = module_path_to_class_path(['not_class_path'])
    assert set(ret) == set(['not_class_path'])

    # Mixture is acceptable.
    ret = module_path_to_class_path(['genuuml.tests.demo', 'object'])
    assert set(ret) == set(['genuuml.tests.demo.Baa', 'genuuml.tests.demo.Baz', 'genuuml.tests.demo.Foo', 'genuuml.tests.demo.Mixin', 'genuuml.tests.demo.MixinFoo', 'object'])


def test_build_registry():
    # Usual class is OK.
    regi, not_founds = build_registry(['genuuml.tests.demo.Foo'])
    assert set(regi.keys()) == set(['builtins.object', 'genuuml.tests.demo.Foo'])

    # Builtin class is also acceptable.
    regi, not_founds = build_registry(['object'])
    assert set(regi.keys()) == set(['builtins.object'])

    # Wrong class path is ignore.
    regi, not_founds = build_registry(['wrong_class_path'])
    assert set(regi.keys()) == set([])

