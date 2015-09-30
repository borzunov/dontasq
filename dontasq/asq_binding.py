#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from abc import ABCMeta

python_version = sys.version_info

if python_version < (3, 3):
    from collections import Iterable
else:
    from collections.abc import Iterable

from asq.queryables import Queryable

from .monkey_patches import extend_type


def get_method_proxy(method):
    def proxy(self, *args, **kwargs):
        return method(Queryable(self), *args, **kwargs)

    proxy.__name__ = method.__name__
    proxy.__doc__ = method.__doc__
    return proxy


def get_asq_methods():
    return dict((name, get_method_proxy(attr))
                for name, attr in vars(Queryable).items()
                if not name.startswith('_') and callable(attr))


asq_methods = get_asq_methods()


def patch_type(klass):
    """
    Extends the class with ``asq.queryables.Queryable`` methods.

    Appends all public methods of ``asq.queryables.Queryable`` to the class
    in such a way that a method call:

        >>> instance.select(lambda x: x * 2)

    Will be equal to:

        >>> Queryable(instance).select(lambda x: x * 2)

    If the class already contains an attribute with a coinciding name
    (e.g. str.join and list.count), this attribute won't be replaced.

    Args:
        klass: A class (but not a metaclass) implements
               ``collection.abc.Iterable`` interface. Can be built-in.

    Raises:
        TypeError: If the argument isn't a class that satisfy
            the requirements above.
    """

    if not isinstance(klass, type):
        raise TypeError('{0} is not a class'.format(klass))
    if isinstance(klass, ABCMeta):
        raise TypeError("{0} can't be a metaclass".format(klass))
    if not issubclass(klass, Iterable):
        raise TypeError('{0} is not iterable'.format(klass))

    extend_type(klass, asq_methods)


def patch_module(module):
    """
    Extends all iterables in the module
    with ``asq.queryables.Queryable`` methods.

    Applies the same as ``patch_type`` to every appropriate member of
    the module.

    Args:
        module: Module object or its __dict__.

    Returns:
        A list of patched classes.
    """

    module_dict = module if isinstance(module, dict) else vars(module)
    patched_types = []
    for klass in module_dict.values():
        if (not isinstance(klass, type) or
                isinstance(klass, ABCMeta) or
                not issubclass(klass, Iterable)):
            continue

        extend_type(klass, asq_methods)
        patched_types.append(klass)
    return patched_types


__all__ = 'patch_type', 'patch_module'
