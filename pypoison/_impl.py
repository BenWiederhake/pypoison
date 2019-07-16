#!/usr/bin/env python3
# Copyright (c) 2019, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.

MAGIC = object()
VIA = (0, None)


def do_raise(reason):
    if VIA[0] == 0:
        raise ValueError('Tried to access {} on poison value.'.format(reason))
    elif VIA[0] == 1:
        raise VIA[1]
    elif VIA[0] == 2:
        raise VIA[1](reason)
    raise AssertionError(VIA[0])


def print_all():
    # `__init__` and `__new__` must be overwritten during `__init__`.
    all_props = [
        'abs', 'add', 'and', 'bool', 'ceil', 'class', 'contains', 'delattr',
        'dict', 'dir', 'div', 'divmod', 'doc', 'eq', 'float', 'floor',
        'floordiv', 'format', 'ge', 'getattribute', 'getitem', 'gt', 'hash',
        'index', 'init_subclass', 'int', 'invert', 'iter', 'le', 'len',
        'lshift', 'lt', 'mod', 'module', 'mul', 'ne', 'neg', 'or', 'pos',
        'pow', 'radd', 'rand', 'rdiv', 'rdivmod', 'reduce', 'reduce_ex',
        'repr', 'rfloordiv', 'rlshift', 'rmod', 'rmul', 'ror', 'round',
        'rpow', 'rrshift', 'rshift', 'rsub', 'rtruediv', 'rxor', 'setattr',
        'sizeof', 'str', 'sub', 'subclasshook', 'truediv', 'trunc', 'xor',
    ]
    for prop in all_props:
        print('    def __{prop}__(*args, **kwargs): do_raise(\'__{prop}__\')\n'.format(prop=prop))


class Poison:
    def __init__(self, magic):
        global MAGIC
        if magic != MAGIC:
            do_raise('__init__ ???')
        MAGIC = object()
        Poison.__init__ = self
        Poison.__new__ = self

    # See 'print_all()'
    def __abs__(*args, **kwargs): do_raise('__abs__')
    def __add__(*args, **kwargs): do_raise('__add__')
    def __and__(*args, **kwargs): do_raise('__and__')
    def __bool__(*args, **kwargs): do_raise('__bool__')
    def __ceil__(*args, **kwargs): do_raise('__ceil__')
    def __class__(*args, **kwargs): do_raise('__class__')
    def __contains__(*args, **kwargs): do_raise('__contains__')
    def __delattr__(*args, **kwargs): do_raise('__delattr__')
    def __dict__(*args, **kwargs): do_raise('__dict__')
    def __dir__(*args, **kwargs): do_raise('__dir__')
    def __div__(*args, **kwargs): do_raise('__div__')
    def __divmod__(*args, **kwargs): do_raise('__divmod__')
    def __doc__(*args, **kwargs): do_raise('__doc__')
    def __eq__(*args, **kwargs): do_raise('__eq__')
    def __float__(*args, **kwargs): do_raise('__float__')
    def __floor__(*args, **kwargs): do_raise('__floor__')
    def __floordiv__(*args, **kwargs): do_raise('__floordiv__')
    def __format__(*args, **kwargs): do_raise('__format__')
    def __ge__(*args, **kwargs): do_raise('__ge__')
    def __getattribute__(*args, **kwargs): do_raise('__getattribute__')
    def __getitem__(*args, **kwargs): do_raise('__getitem__')
    def __gt__(*args, **kwargs): do_raise('__gt__')
    def __hash__(*args, **kwargs): do_raise('__hash__')
    def __index__(*args, **kwargs): do_raise('__index__')
    def __init_subclass__(*args, **kwargs): do_raise('__init_subclass__')
    def __int__(*args, **kwargs): do_raise('__int__')
    def __invert__(*args, **kwargs): do_raise('__invert__')
    def __iter__(*args, **kwargs): do_raise('__iter__')
    def __le__(*args, **kwargs): do_raise('__le__')
    def __len__(*args, **kwargs): do_raise('__len__')
    def __lshift__(*args, **kwargs): do_raise('__lshift__')
    def __lt__(*args, **kwargs): do_raise('__lt__')
    def __mod__(*args, **kwargs): do_raise('__mod__')
    def __module__(*args, **kwargs): do_raise('__module__')
    def __mul__(*args, **kwargs): do_raise('__mul__')
    def __ne__(*args, **kwargs): do_raise('__ne__')
    def __neg__(*args, **kwargs): do_raise('__neg__')
    def __or__(*args, **kwargs): do_raise('__or__')
    def __pos__(*args, **kwargs): do_raise('__pos__')
    def __pow__(*args, **kwargs): do_raise('__pow__')
    def __radd__(*args, **kwargs): do_raise('__radd__')
    def __rand__(*args, **kwargs): do_raise('__rand__')
    def __rdiv__(*args, **kwargs): do_raise('__rdiv__')
    def __rdivmod__(*args, **kwargs): do_raise('__rdivmod__')
    def __reduce__(*args, **kwargs): do_raise('__reduce__')
    def __reduce_ex__(*args, **kwargs): do_raise('__reduce_ex__')
    def __repr__(*args, **kwargs): do_raise('__repr__')
    def __rfloordiv__(*args, **kwargs): do_raise('__rfloordiv__')
    def __rlshift__(*args, **kwargs): do_raise('__rlshift__')
    def __rmod__(*args, **kwargs): do_raise('__rmod__')
    def __rmul__(*args, **kwargs): do_raise('__rmul__')
    def __ror__(*args, **kwargs): do_raise('__ror__')
    def __round__(*args, **kwargs): do_raise('__round__')
    def __rpow__(*args, **kwargs): do_raise('__rpow__')
    def __rrshift__(*args, **kwargs): do_raise('__rrshift__')
    def __rshift__(*args, **kwargs): do_raise('__rshift__')
    def __rsub__(*args, **kwargs): do_raise('__rsub__')
    def __rtruediv__(*args, **kwargs): do_raise('__rtruediv__')
    def __rxor__(*args, **kwargs): do_raise('__rxor__')
    def __setattr__(*args, **kwargs): do_raise('__setattr__')
    def __sizeof__(*args, **kwargs): do_raise('__sizeof__')
    def __str__(*args, **kwargs): do_raise('__str__')
    def __sub__(*args, **kwargs): do_raise('__sub__')
    def __subclasshook__(*args, **kwargs): do_raise('__subclasshook__')
    def __truediv__(*args, **kwargs): do_raise('__truediv__')
    def __trunc__(*args, **kwargs): do_raise('__trunc__')
    def __xor__(*args, **kwargs): do_raise('__xor__')


def set_exception(custom_exception):
    global VIA
    if custom_exception is None:
        VIA = (0, None)
    else:
        VIA = (1, custom_exception)


def set_handler(custom_handler):
    global VIA
    VIA = (2, custom_handler)


# Avoid storing it in a global, as many modules touch
# every global module attribute, e.g. unittest.
def get_poison_from(magic=[]):
    if not magic:
        magic.append(Poison(MAGIC))
    return magic[0]


def get_poison():
    return get_poison_from()
