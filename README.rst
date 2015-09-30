=======
dontasq
=======

Extend built-in Python collections with LINQ-for-objects style methods

Description
-----------

The library extends built-in Python collections with methods from `Robert Smallshire`_'s asq_. Adding methods to built-ins isn't officially allowed, but it's possible to do this in CPython (both 2.x and 3.x) using a hack described in the corresponding section below.

.. _Robert Smallshire: https://github.com/rob-smallshire
.. _asq: https://github.com/rob-smallshire/asq

For example:

.. code:: python

    >>> import dontasq
    >>>
    >>> [1, 2, 3].select_many(lambda x: (x, x ** 2)).to_tuple()
    (1, 1, 2, 4, 3, 9)
    >>> 'oh brave new world'.split() \
    ...                     .where(lambda word: len(word) >= 5) \
    ...                     .select(str.capitalize) \
    ...                     .to_list()
    ['Brave', 'World']

In some cases, this style helps to write functional-esque code that is more clear than code with ``map``, ``filter`` and generator expressions: there's no confusion with brackets, and methods are applied in the natural order.

**Warning!** ``dontasq`` uses undocumented CPython features. It's not guaranteed that this features will be maintained in the future Python versions.

Details
-------

During import, ``dontasq`` looks for classes in the built-ins namespace, ``collections`` and ``itertools`` modules. If a class is an iterable and isn't a metaclass, the library will append all public methods of ``asq.queryables.Queryable`` to it in such a way that a method call:

.. code:: python

    >>> instance.select(lambda x: x * 2)

Will be equal to:

.. code:: python

    >>> Queryable(instance).select(lambda x: x * 2)

So the methods will be added to classes such as ``list``, ``str``, ``collections.OrderedDict``, or ``itertools.count``. You can find a list of all ``Queryable`` methods and their description in `asq documentation`_.

.. _asq documentation: http://docs.asq.googlecode.com/hg/1.0/html/reference/queryables.html#asq-queryables-queryable

If a class already contains an attribute with a coinciding name (e.g. ``str.join`` and ``list.count``), this attribute won't be replaced.

Of course, you're able to import other ``asq`` modules when using ``dontasq``:

.. code:: python

    >>> import dontasq
    >>> from asq.predicates import *
    >>>
    >>> words = ['banana', 'receive', 'believe', 'ticket', 'deceive']
    >>> words.where(contains_('ei')).to_list()
    ['receive', 'deceive']

If you want to patch classes from another library, you can use methods ``dontasq.patch_type`` and ``dontasq.patch_module``:

.. code:: python

    >>> import bintrees
    >>> import dontasq
    >>>
    >>> dontasq.patch_type(bintrees.AVLTree)
    >>>
    >>> dictionary = {1: 'Anton', 2: 'James', 3: 'Olivia'}
    >>> bintrees.AVLTree(dictionary).select(lambda x: x * 2).to_list()
    [2, 4, 6]

You can find other examples in `"tests" directory`_.

.. _"tests" directory: https://github.com/borzunov/dontasq/tree/master/tests

Adding methods to built-ins
---------------------------

The following approach is found in `this question`_ on StackOverflow.

.. _this question: https://stackoverflow.com/questions/25440694/whats-the-purpose-of-dictproxy

Officially, you can get only a protected (read-only) instance of built-ins' ``__dict__``. The trick is that in CPython this instance contains a reference to an original (modifiable) dictionary that can be tracked with `gc.get_referents`_ function.

.. _gc.get_referents: https://docs.python.org/3/library/gc.html#gc.get_referents

For example, we can add ``select`` method to built-in ``list`` (unlike ``dontasq``, it's non-lazy in this example):

.. code:: python

  >>> import gc
  >>> gc.get_referents(vars(list))[0]['select'] = lambda self, func: list(map(func, self))
  >>>
  >>> [1, 2, 3].select(lambda x: x * 2)
  [2, 4, 6]

Another possible way is to use forbiddenfruit_ library that interacts with ``ctypes.pythonapi`` module. The both approaches stably work on both Python 2 and 3, but restricted to CPython only.

.. _forbiddenfruit: https://github.com/clarete/forbiddenfruit

Installation
------------

You can install the library using pip::

    sudo pip install dontasq

Or install a previously downloaded and extracted package::

    sudo python setup.py install

Authors
-------

Copyright (c) 2015 Alexander Borzunov

The library name suggested by `Robert Smallshire`_ (an author of `asq`_).
