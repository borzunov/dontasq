#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extend built-in Python collections with LINQ-for-objects style methods

During import, extends all iterables in the built-ins namespace,
``collections`` and ``itertools`` modules with ``asq.queryables.Queryable``
methods.
"""

import collections
import itertools

from .asq_binding import patch_module, patch_type


__author__ = 'Alexander Borzunov'
__version__ = '0.1'


patch_module(__builtins__)
patch_type(type({}.keys()))
patch_type(type({}.values()))
patch_type(type({}.items()))
patch_module(collections)
patch_module(itertools)


__all__ = 'patch_type', 'patch_module'
