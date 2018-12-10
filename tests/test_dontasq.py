#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import itertools
import unittest

import dontasq


class MethodsTest(unittest.TestCase):
    def test_builtins(self):
        actual = [1, 2, 4, 10, 20, 65] \
            .where(lambda x: x % 2 == 0) \
            .select(lambda x: x * 2) \
            .to_list()
        expected = [4, 8, 20, 40]
        self.assertEqual(expected, actual)

        actual = (-6, 2, 5) \
            .select_many(lambda x: [x, x ** 2]) \
            .to_tuple()
        expected = (-6, 36, 2, 4, 5, 25)
        self.assertEqual(expected, actual)

        actual = 'Australia Canada Russia' \
            .split() \
            .to_dictionary(key_selector=lambda word: word[:2].upper())
        expected = {
            'AU': 'Australia',
            'CA': 'Canada',
            'RU': 'Russia',
        }
        self.assertEqual(expected, actual)

        actual = 'Formula1'.all(str.isalnum)
        expected = True
        self.assertEqual(expected, actual)

    def test_dict_methods(self):
        dictionary = {12: 22, 20: 2, 30: 3, 88: 2}

        actual = dictionary.keys().sum()
        expected = 150
        self.assertEqual(expected, actual)

        actual = dictionary.values() \
                           .distinct() \
                           .order_by() \
                           .to_list()
        expected = [2, 3, 22]
        self.assertEqual(expected, actual)

    def test_collections(self):
        order = collections.deque()
        order.append(5)
        order.appendleft(3)
        order.appendleft(6)

        actual = order.select(lambda x: x + 2).to_list()
        expected = [8, 5, 7]
        self.assertEqual(expected, actual)

    def test_itertools(self):
        actual = itertools.count(1) \
                          .select(lambda x: x * 3 - 2) \
                          .take(6) \
                          .to_list()
        expected = [1, 4, 7, 10, 13, 16]
        self.assertEqual(expected, actual)


class QueryTest(unittest.TestCase):
    def test_builtins(self):
        actual = [1, 2, 4, 10, 20, 65].query() \
            .where(lambda x: x % 2 == 0) \
            .select(lambda x: x * 2) \
            .to_list()
        expected = [4, 8, 20, 40]
        self.assertEqual(expected, actual)

        actual = (-6, 2, 5).query() \
            .select_many(lambda x: [x, x ** 2]) \
            .to_tuple()
        expected = (-6, 36, 2, 4, 5, 25)
        self.assertEqual(expected, actual)

        actual = 'Australia Canada Russia' \
            .split() \
            .query() \
            .to_dictionary(key_selector=lambda word: word[:2].upper())
        expected = {
            'AU': 'Australia',
            'CA': 'Canada',
            'RU': 'Russia',
        }
        self.assertEqual(expected, actual)

        actual = 'Formula1'.query().all(str.isalnum)
        expected = True
        self.assertEqual(expected, actual)

        actual = 'abcdef'.query().to_list()
        expected = ['a', 'b', 'c', 'd', 'e', 'f']
        self.assertEqual(expected, actual)

        test_str = 'kgsfidj_ddf'
        self.assertEqual(len(test_str), test_str.query().count())

    def test_dict_methods(self):
        dictionary = {12: 22, 20: 2, 30: 3, 88: 2}

        actual = dictionary.keys().query().sum()
        expected = 150
        self.assertEqual(expected, actual)

        actual = dictionary.values().query() \
                           .distinct() \
                           .order_by() \
                           .to_list()
        expected = [2, 3, 22]
        self.assertEqual(expected, actual)

    def test_collections(self):
        order = collections.deque()
        order.append(5)
        order.appendleft(3)
        order.appendleft(6)

        actual = order.query().select(lambda x: x + 2).to_list()
        expected = [8, 5, 7]
        self.assertEqual(expected, actual)

    def test_itertools(self):
        actual = itertools.count(1).query() \
                          .select(lambda x: x * 3 - 2) \
                          .take(6) \
                          .to_list()
        expected = [1, 4, 7, 10, 13, 16]
        self.assertEqual(expected, actual)


class CollisionTest(unittest.TestCase):
    def test_collision(self):
        actual = ', '.join(['London', 'Paris'])
        expected = 'London, Paris'
        self.assertEqual(expected, actual)

        actual = ['Masha', 'Alice'] \
            .join(['Ann', 'Misha'],
                  inner_key_selector=lambda name: name[0],
                  outer_key_selector=lambda name: name[0])
        expected = [('Masha', 'Misha'), ('Alice', 'Ann')]
        self.assertEqual(expected, actual)


class ProblemsTest(unittest.TestCase):
    @staticmethod
    def get_most_frequent_words(text, count):
        """Problem from a LINQ course:
        https://ulearn.azurewebsites.net/Course/Linq

        Return *count* the most frequent words contained in *text* with their
        frequency. Prefer lexicographically lesser words among words with
        the same frequency. Compare words case-insensetively and output them
        in the lower case.
        """

        return text.split() \
                   .group_by(str.lower) \
                   .select(lambda g: (g.key, g.count())) \
                   .order_by_descending(lambda x: x[1]) \
                   .then_by(lambda x: x[0]) \
                   .take(count) \
                   .to_list()

    def test_most_frequent_words(self):
        text = ('A box of biscuits, a box of mixed biscuits, '
                'and a biscuit mixer.')
        actual = ProblemsTest.get_most_frequent_words(text, 4)
        expected = [('a', 3), ('biscuits,', 2), ('box', 2), ('of', 2)]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
