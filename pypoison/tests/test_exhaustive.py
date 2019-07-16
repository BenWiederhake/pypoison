#!/usr/bin/env python3
# Copyright (c) 2019, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.

import pypoison
import unittest


# Don't store this in a global: `unittest` would choke.
def poison():
    return pypoison.get_poison()


# TODO untested: 'ceil', 'class', 'dict', 'div', 'doc', 'floor', 'module'
# TODO untested: 'rdiv', 'reduce', 'reduce_ex', 'sizeof', 'subclasshook'
class TestMethods(unittest.TestCase):
    CASES_VALUE_ERROR = [
        ('abs', lambda: abs(poison())),
        ('add', lambda: poison() + 1),
        ('and', lambda: poison() & 7),
        ('bool', lambda: bool(poison())),
        ('contains', lambda: 1 in poison()),
        ('delattr', lambda: delattr(poison(), 'asdf')),
        ('dir', lambda: dir(poison())),
        ('divmod', lambda: divmod(poison(), 4)),
        ('eq', lambda: poison() == 3),
        ('float', lambda: float(poison())),
        ('floordiv', lambda: poison() // 2),
        ('format', lambda: '{}'.format(poison())),
        ('format', lambda: format(poison())),
        ('ge', lambda: poison() >= 5),
        ('getattribute', lambda: poison().asdf),
        ('getattribute', lambda: poison().__dict__),
        ('getattribute', lambda: poison().__dir__),
        ('getattribute', lambda: getattr(poison(), 'qwer')),
        ('getitem', lambda: poison()[6]),
        ('getitem', lambda: poison()['foo']),
        ('gt', lambda: poison() > 7),
        ('gt', lambda: 8 < poison()),
        ('hash', lambda: hash(poison())),
        ('hash', lambda: {poison(): 4}),
        ('hash', lambda: {5: 4}[poison()]),
        ('index', lambda: [4, -2, 1][poison()]),
        ('int', lambda: int(poison())),
        ('invert', lambda: ~poison()),
        ('iter', lambda: list(poison())),
        ('iter', lambda: set(poison())),
        ('iter', lambda: enumerate(poison())),
        ('le', lambda: poison() <= 9),
        ('len', lambda: len(poison())),
        ('lshift', lambda: poison() << 10),
        ('lt', lambda: poison() < 10),
        ('mod', lambda: poison() % 10),
        ('mod', lambda: poison() % (3, '5', 0.01)),
        ('mul', lambda: poison() * 8),
        ('ne', lambda: poison() != 6),
        ('neg', lambda: -poison()),
        ('or', lambda: poison() | 11),
        ('pos', lambda: +poison()),
        ('pow', lambda: poison() ** 12),
        ('radd', lambda: 13 + poison()),
        ('rand', lambda: 13 & poison()),
        ('rdivmod', lambda: divmod(13, poison())),
        ('repr', lambda: repr(poison())),
        ('repr', lambda: '{!r}'.format(poison())),
        ('rfloordiv', lambda: 13 // poison()),
        ('rlshift', lambda: 14 << poison()),
        ('rmod', lambda: 15 % poison()),
        ('rmul', lambda: 16 * poison()),
        ('ror', lambda: 16 | poison()),
        ('round', lambda: round(poison())),
        ('rpow', lambda: 1.01 ** poison()),
        ('rpow', lambda: 16 ** poison()),
        ('rrshift', lambda: 16 >> poison()),
        ('rshift', lambda: poison() >> 1),
        ('rsub', lambda: 9999 - poison()),
        ('rtruediv', lambda: 17 / poison()),
        ('rxor', lambda: 18 ^ poison()),
        ('setattr', lambda: setattr(poison(), 'quux', 'snafu')),
        ('str', lambda: str(poison())),
        ('sub', lambda: poison() - 18),
        ('truediv', lambda: poison() / 19),
        ('xor', lambda: poison() ^ 20),
    ]

    def setUp(self):
        pypoison.set_exception(None)

    def test_value_error(self):
        for prop, lambda_ in TestMethods.CASES_VALUE_ERROR:
            with self.subTest(prop=prop) as subtest:
                try:
                    lambda_()
                except ValueError as e:
                    self.assertEqual('Tried to access __{}__ on poison value.'.format(prop), e.args[0])
                except BaseException as e:
                    self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, e))
                else:
                    self.fail('Expected exception about __{}__, passed instead.'.format(prop))

    def test_setattr_long(self):
        prop = 'setattr'
        try:
            poison().bar = 'baz'
        except ValueError as e:
            self.assertEqual('Tried to access __{}__ on poison value.'.format(prop), e.args[0])
        except BaseException as e:
            self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, e))
        else:
            self.fail('Expected exception about __{}__, passed instead.'.format(prop))

    def test_init_subclass_long(self):
        prop = 'init_subclass'
        try:
            class Foo(pypoison._impl.Poison):
                def foo(self):
                    print('yay')
        except ValueError as e:
            self.assertEqual('Tried to access __{}__ on poison value.'.format(prop), e.args[0])
        except BaseException as e:
            self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, e))
        else:
            self.fail('Expected exception about __{}__, passed instead.'.format(prop))
