#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
from collections import MutableMapping


def extend_dict(type_dict, attrs):
    for name, attr in attrs.items():
        if name not in type_dict:
            # TODO: Write in the docs about the IF
            type_dict[name] = attr


def extend_builtin_type(klass, attrs):
    # An interesting hack from:
    #     https://stackoverflow.com/questions/25440694/whats-the-purpose-of-dictproxy

    referents = gc.get_referents(klass.__dict__)
    if not (len(referents) == 1 and isinstance(referents[0], dict)):
        raise ValueError("Can't find writable __dict__ instance for {0}"
                         .format(klass))
    extend_dict(referents[0], attrs)


def extend_type(klass, attrs):
    klass_dict = vars(klass)
    if isinstance(klass_dict, MutableMapping):
        extend_dict(klass_dict, attrs)
    else:
        extend_builtin_type(klass, attrs)


__all__ = 'extend_type'
