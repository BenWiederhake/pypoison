#!/usr/bin/env python3
# Copyright (c) 2019, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.

import pypoison
import sys
import unittest


DEBUG_TESTS = False
PYV = (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)


# Don't store this in a global: `unittest` would choke.
def poison():
    return pypoison.get_poison()


# TODO untested: 'ceil', 'class', 'dict', 'div', 'doc', 'floor', 'module'
# TODO untested: 'rdiv', 'reduce', 'reduce_ex', 'sizeof', 'subclasshook'
class TestMethods(unittest.TestCase):
    CASES = [
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
        ('len' if PYV >= (3, 8, 0) else 'iter', lambda: list(poison())),
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

    def test_simple(self):
        for i, (prop, lambda_) in enumerate(TestMethods.CASES):
            with self.subTest(i=i, prop=prop) as subtest:
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
        actual = ('Pass', None)
        try:
            class Foo(pypoison._impl.Poison):
                def foo(self):
                    print('yay')
        except ValueError as e:
            actual = ('ValueError', e.args)
        except BaseException as e:
            actual = ('Other', e)

        if PYV >= (3, 6, 0):
            # __init_subclass__ got introduced in PEP 487, which got incorporated in 3.6.0.
            expected = ('ValueError', ('Tried to access __init_subclass__ on poison value.',))
        else:
            # Should not call it (yet).
            expected = ('Pass', None)
        self.assertEqual(expected, actual)


# TODO untested: breakpoint, compile, exec, globals, locals, open, super
# However, I pinky-promise that these either just don't take arguments,
# or fail immediately.
class TestBuiltins(unittest.TestCase):
    CASES_VALUE_ERROR = [
        ('abs', lambda: abs(poison())),
        ('iter', lambda: all(poison())),
        ('repr', lambda: ascii(poison())),
        ('index', lambda: bin(poison())),
        ('bool', lambda: bool(poison())),
        ('index' if PYV >= (3, 8, 0) else 'int', lambda: chr(poison())),
        ('float', lambda: complex(poison())),
        ('delattr', lambda: delattr(poison(), 'foo')),
        ('getattribute' if PYV >= (3, 7, 0) else 'iter', lambda: dict(poison())),
        ('dir', lambda: dir(poison())),
        ('divmod', lambda: divmod(poison(), 42)),
        ('rdivmod', lambda: divmod(42, poison())),
        ('iter', lambda: enumerate(poison())),
        ('iter', lambda: filter(None, poison())),
        ('float', lambda: float(poison())),
        ('format', lambda: format(poison())),
        ('iter', lambda: frozenset(poison())),
        ('getattribute', lambda: getattr(poison(), 'bar')),
        ('getattribute', lambda: hasattr(poison(), 'quux')),
        ('hash', lambda: hash(poison())),
        ('getattribute', lambda: help(poison())),
        ('index', lambda: hex(poison())),
        ('int', lambda: int(poison())),
        ('str', lambda: input(poison())),
        ('getattribute', lambda: isinstance(poison(), str)),
        ('getattribute', lambda: isinstance(4, poison())),
        ('getattribute', lambda: issubclass(poison(), str)),
        ('getattribute', lambda: issubclass(str, poison())),
        ('iter', lambda: iter(poison())),
        ('len', lambda: len(poison())),
        ('len' if PYV >= (3, 8, 0) else 'iter', lambda: list(poison())),
        ('iter', lambda: map(id, poison())),
        ('iter', lambda: max(poison())),
        ('iter', lambda: min(poison())),
        ('index', lambda: oct(poison())),
        ('pow', lambda: pow(poison(), 3)),
        ('rpow', lambda: pow(3, poison())),
        ('str', lambda: print(poison())),
        ('index', lambda: range(poison())),
        ('index', lambda: range(1, poison())),
        ('index', lambda: range(poison(), 3)),
        ('index', lambda: range(1, poison(), 3)),
        ('index', lambda: range(poison(), 42, 3)),
        ('repr', lambda: repr(poison())),
        ('len', lambda: reversed(poison())),
        ('round', lambda: round(poison())),
        ('iter', lambda: set(poison())),
        ('setattr', lambda: setattr(poison(), 'asdf', 'qwer')),
        ('iter', lambda: sorted(poison())),
        ('str', lambda: str(poison())),
        ('iter', lambda: sum(poison())),
        ('iter', lambda: tuple(poison())),
        ('iter', lambda: zip(poison())),
        ('iter', lambda: zip([3], poison())),
    ]

    CASES_TYPE_ERROR = [
        ('eval() arg 1 must be a string, bytes or code object', eval),
        ("memoryview: a bytes-like object is required, not 'Poison'", memoryview),
        ("'Poison' object is not an iterator", next),
        ('object() takes no arguments' if PYV >= (3, 7, 0) else 'object() takes no parameters', object),
        ('ord() expected string of length 1, but Poison found', ord),
        ('__import__() argument 1 must be str, not Poison', __import__),
    ]

    CASES_SUCCESS = [
        ([], lambda: list(filter(poison(), []))),

        # Currently, the following tests are declared as "unsure".  These calls
        # *should* raise an exception, but I don't yet know how.
        (False, lambda: callable(poison())),
        ('undescribable', lambda: id(poison())),
        (pypoison._impl.Poison, lambda: type(poison())),

        # I don't like that the following tests pass,
        # but they seem to only store the argument without doing anything.
        ('undescribable', lambda: classmethod(poison())),
        ('undescribable', lambda: staticmethod(poison())),
        ('undescribable', lambda: slice(poison())),
        ('undescribable', lambda: slice(poison(), 3)),
        ('undescribable', lambda: slice(1, poison())),
        ('undescribable', lambda: slice(poison(), 3, 2)),
        ('undescribable', lambda: slice(1, poison(), 2)),
    ]

    @classmethod
    def setUpClass(cls):
        pypoison.set_exception(None)

        # ==== Weird behavior changes: ====

        # == `vars`:
        if PYV >= (3, 8, 0):
            # 3.8.0: accesses `__getattribute__`, raises *Value*Error.
            TestBuiltins.CASES_VALUE_ERROR.append(('getattribute', lambda: vars(poison())))
        else:
            # 3.7.5 and down: accesses `__dict__`, raises custom *Type*Error.
            TestBuiltins.CASES_TYPE_ERROR.append(('vars() argument must have __dict__ attribute', vars))

        # == `property`:
        if PYV >= (3, 8, 0):
            # 3.8.0: accesses `__getattribute__`, raises ValueError.
            TestBuiltins.CASES_VALUE_ERROR.append(('getattribute', lambda: property(poison())))
        else:
            # 3.7.5 and down: no accesses at all.
            TestBuiltins.CASES_SUCCESS.append(('undescribable', lambda: property(poison())))


    def test_bytearray(self):
        # See `test_prints`.
        props = ['index', 'iter']
        try:
            bytearray(poison())
        except ValueError as e:
            self.assertEqual(1, len(e.args))
            expected = ['Tried to access __{}__ on poison value.'.format(p) for p in props]
            self.assertIn(e.args[0], expected)
        except BaseException as e:
            self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, repr(e)))
        else:
            self.fail('Expected exception about __{}__, passed instead.'.format(prop))

    def test_bytes(self):
        # See `test_prints`.
        props = ['index', 'len']
        try:
            bytes(poison())
        except ValueError as e:
            self.assertEqual(1, len(e.args))
            expected = ['Tried to access __{}__ on poison value.'.format(p) for p in props]
            self.assertIn(e.args[0], expected)
        except TypeError as e:
            self.assertEqual(e.args[0], "cannot convert 'Poison' object to bytes")
        except BaseException as e:
            self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, repr(e)))
        else:
            self.fail('Expected exception about __{}__, passed instead.'.format(prop))

    def test_value_error(self):
        for i, (prop, lambda_) in enumerate(TestBuiltins.CASES_VALUE_ERROR):
            with self.subTest(i=i, prop=prop) as subtest:
                try:
                    lambda_()
                except ValueError as e:
                    self.assertEqual(1, len(e.args))
                    expected = 'Tried to access __{}__ on poison value.'.format(prop)
                    self.assertEqual(e.args[0], expected)
                except BaseException as e:
                    self.fail('Expected exception about __{}__, got "{}" instead.'.format(prop, repr(e)))
                else:
                    self.fail('Expected exception about __{}__, passed instead.'.format(prop))

    def test_type_error(self):
        for msg, fn in TestBuiltins.CASES_TYPE_ERROR:
            with self.subTest(fn=fn) as subtest:
                try:
                    fn(poison())
                except TypeError as e:
                    self.assertEqual(1, len(e.args))
                    self.assertEqual(e.args[0], msg)
                except BaseException as e:
                    self.fail('Expected TypeError({}), got "{}" instead.'.format(msg, repr(e)))
                else:
                    self.fail('Expected TypeError({}), passed instead.'.format(msg))

    def test_success(self):
        for i, (expected, lambda_) in enumerate(TestBuiltins.CASES_SUCCESS):
            with self.subTest(i=i) as subtest:
                actual = lambda_()
                if expected == 'undescribable':
                    self.assertNotEqual(expected, actual)
                else:
                    self.assertEqual(expected, actual)

    @unittest.skipIf(not DEBUG_TESTS, reason='DEBUG_TESTS not set')
    def test_prints(self):
        print('Version:', PYV)
        LAMBDAS = [
            lambda: bytearray(poison()),
            # Version: (3, 5, 6) → Tried to access __iter__ on poison value.
            # Version: (3, 6, 3) → Tried to access __iter__ on poison value.
            # Version: (3, 6, 8) → Tried to access __index__ on poison value.
            # Version: (3, 7, 1) → Tried to access __iter__ on poison value.
            # Version: (3, 7, 3) → Tried to access __index__ on poison value.
            # Version: (3, 8, 0) → Tried to access __index__ on poison value.
            lambda: bytes(poison()),
            # Version: (3, 5, 6) → Tried to access __len__ on poison value.
            # Version: (3, 6, 3) → cannot convert 'Poison' object to bytes
            # Version: (3, 6, 8) → Tried to access __index__ on poison value.
            # Version: (3, 7, 1) → cannot convert 'Poison' object to bytes
            # Version: (3, 7, 3) → Tried to access __index__ on poison value.
            # Version: (3, 8, 0) → Tried to access __index__ on poison value.
            lambda: dict(poison()),
            # Version: (3, 5, 6) → Tried to access __iter__ on poison value.
            # Version: (3, 6, 3) → Tried to access __iter__ on poison value.
            # Version: (3, 6, 8) → Tried to access __iter__ on poison value.
            # Version: (3, 7, 1) → Tried to access __getattribute__ on poison value.
            # Version: (3, 7, 3) → Tried to access __getattribute__ on poison value.
            # Version: (3, 8, 0) → Tried to access __getattribute__ on poison value.
            # Seems to depend on whether insertion order is guaranteed.  Great!
        ]

        for i, l in enumerate(LAMBDAS):
            try:
                l()
            except BaseException as e:
                print(i, e)
            else:
                print(i, 'Pass')
        print('Done')
        # Ensure we get printed
        raise AssertionError('Boo!')
