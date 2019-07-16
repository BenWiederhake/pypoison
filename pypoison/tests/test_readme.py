#!/usr/bin/env python3
# Copyright (c) 2019, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.

import pypoison
import unittest


# Don't store this in a global: `unittest` would choke.
def poison():
    return pypoison.get_poison()


# FIXME: TEST THIS!
# By default, all accesses raise a `ValueError` with a human-readable
# explanation which attribute/method was accessed.
#
# If you prefer otherwise, you can call `pypoison.set_exception(my_exception)`,
# and the poison value now raises the object `my_exception`
# whenever anything is done with the poison value.
#
# For extra fanciness, you can call `pypoison.set_handler(my_fn)`,
# and the poison value will raise whatever `my_fn(method_name)` returns.
#
# To reset to the default behavior, you can call `pypoison.set_exception(None)`



class TestFails(unittest.TestCase):
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
        for prop, lambda_ in TestFails.DATA:
            with self.subTest(prop=prop) as subtest:
                try:
                    lambda_()
                except ValueError as e:
                    self.assertEqual('Tried to access __{}__ on poison value.'.format(prop), e.args[0])
                except BaseException as e:
                    self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, e))
                else:
                    self.fail('Expected exception about __{}__, passed instead.'.format(prop))
