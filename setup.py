#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup


project_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(project_dir, 'dontasq', '__init__.py')) as f:
    version = re.search(r"__version__ = '(.+)'", f.read()).groups()[0]

with open(os.path.join(project_dir, 'README.rst')) as f:
    long_description = f.read()

setup(
    name="dontasq",
    version=version,
    packages=['dontasq'],

    install_requires=['asq>=1.0'],

    author="Alexander Borzunov",
    author_email="borzunov.alexander@gmail.com",

    description='Extend built-in Python collections '
                'with LINQ-for-objects style methods',
    long_description=long_description,
    url="https://github.com/borzunov/dontasq",

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license="MIT",
    keywords=['LINQ'],

    test_suite='tests',
)
