#!/usr/bin/env python3
# Copyright (c) 2019, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.

import pypoison
import unittest


# Don't store this in a global: `unittest` would choke.
def poison():
    return pypoison.get_poison()


class TestBasic(unittest.TestCase):
    def setUp(self):
        pypoison.set_exception(None)

    def test_identity(self):
        self.assertIs(poison(), poison())

    def test_readable(self):
        try:
            x = poison() + 3
        except ValueError as e:
            self.assertEqual(e.args, ('Tried to access __add__ on poison value.',))


class TestBehavior(unittest.TestCase):
    def test_exception(self):
        pypoison.set_exception(KeyError('Surprise!'))
        try:
            x = poison() + 3
        except KeyError as e:
            self.assertEqual(e.args, ('Surprise!',))
        # Does it work a second time?
        try:
            x = poison() + 3
        except KeyError as e:
            self.assertEqual(e.args, ('Surprise!',))
        # Can we reset?
        pypoison.set_exception(None)
        try:
            x = poison() + 3
        except ValueError as e:
            self.assertEqual(e.args, ('Tried to access __add__ on poison value.',))

    def test_handler(self):
        def my_handler(reason, time=[-1]):
            time[0] += 1
            return KeyError('handler', reason, time[0])

        pypoison.set_handler(my_handler)
        try:
            x = poison() + 3
        except KeyError as e:
            self.assertEqual(e.args, ('handler', '__add__', 0))
        try:
            x = poison() + 3
        except KeyError as e:
            self.assertEqual(e.args, ('handler', '__add__', 1))


class TestExamples(unittest.TestCase):
    DATA = [
        ('contains', lambda: 1 in poison()),
        ('truediv', lambda: poison() / 1),
        ('radd', lambda: 1 + poison()),
        ('mul', lambda: poison() * 4),
        ('mod', lambda: poison() % 3),
        ('rmod', lambda: 3 % poison()),
        ('format', lambda: '{}'.format(poison())),
        ('repr', lambda: '{!r}'.format(poison())),
        ('iter', lambda: list(poison())),
        ('getattribute', lambda: help(poison())),
        ('eq', lambda: poison() == 42),
    ]

    def setUp(self):
        pypoison.set_exception(None)

    def test_fails(self):
        for prop, lambda_ in TestExamples.DATA:
            with self.subTest(prop=prop) as subtest:
                try:
                    lambda_()
                except ValueError as e:
                    self.assertEqual('Tried to access __{}__ on poison value.'.format(prop), e.args[0])
                except BaseException as e:
                    self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, e))
                else:
                    self.fail('Expected exception about __{}__, passed instead.'.format(prop))

    def test_successes(self):
        self.assertIs(poison(), poison())
        l = [poison(), poison()]
        self.assertEqual(len(l), 2)

    def test_unsure(self):
        # Currently, these tests are declared as "unsure".  These calls
        # *should* raise an exception, but I don't yet know how.

        # callable():
        self.assertFalse(callable(poison()))
        # id():
        self.assertNotEqual(id(poison()), 'lolwut')
        # type():
        self.assertNotEqual(type(poison()), int)

    def test_undetectable(self):
        # If these fail:
        # - Hooray!  I can detect logically-null ussages!
        # - But do we want that?
        # - Also, how the hell did you do that?
        self.assertFalse(poison() in [])
        self.assertTrue(True or poison())
        self.assertFalse(False and poison())
        self.assertIs(poison(), max([pypoison.get_poison()]))
