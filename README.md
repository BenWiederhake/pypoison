# pypoison

> Nothing says "DO NOT USE" like a poison value.

Sometimes you need a value to represent absence of a value.
However, sometimes you want to make absolutely sure this value is not used in any way, shape, form, or anything whatsoever.
In these cases, values like `None`, `float('NaN')`, or `False` don't really fit, because you can still "touch" these values.

That's what poison values are for.
Because nothing says "DO NOT USE" like a poison value.

This module provides an object that overrides all methods to raise an exception.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Caveats](#caveats)
- [TODOs](#todos)
- [Contribute](#contribute)

## Install

Just `pip install pypoison`. (As soon as I have uploaded it to PyPI.)

Or just copy `pypoison/__init__.py` to your project as `pypoison.py`.

There are no dependencies.

## Usage

Just use the value `pypoison.POISON` when you need a poison value.

### Custom behavior

By default, all accesses raise a `ValueError` with a human-readable
explanation which attribute/method was accessed.

If you prefer otherwise, you can call `pypoison.set_exception(my_exception)`,
and the poison value now raises the object `my_exception`
whenever anything is done with the poison value.

For extra fanciness, you can call `pypoison.set_handler(my_fn)`,
and the poison value will raise whatever `my_fn(method_name)` returns.

To reset to the default behavior, you can call `pypoison.set_exception(None)`

### Examples

```python
>>> 1 in pypoison.POISON
ValueError: Tried to access __contains__ on poison value.
>>> pypoison.POISON / 1
ValueError: Tried to access __div__ on poison value.
>>> 1 + Foo()
ValueError: Tried to access __radd__ on poison value.
>>> pypoison.POISON * 4
ValueError: Tried to access __mul__ on poison value.
>>> pypoison.POISON % 3
ValueError: Tried to access __mod__ on poison value.
>>> 3 % pypoison.POISON
ValueError: Tried to access __rmod__ on poison value.
>>> '{}'.format(pypoison.POISON)
ValueError: Tried to access __format__ on poison value.
>>> '{!r}'.format(pypoison.POISON)
ValueError: Tried to access __repr__ on poison value.
>>> list(pypoison.POISON)
ValueError: Tried to access __iter__ on poison value.
>>> help(pypoison.POISON)
ValueError: Tried to access __getattribute__ on poison value.
>>> pypoison.POISON == 42
ValueError: Tried to access __eq__ on poison value.
```

## Caveat

### Serious

Heavy use of the `inspect` module might fiddle around with `pypoison.POISON`, however
safeguards are in place to make sure that accidental calls result in exceptions.

Accidental assignment to `pypoison.POISON` is still possible.
[This can be prevented.](https://stackoverflow.com/a/3712574/3070326)

Passive use, such as `is` or storing a pointer cannot be prevented.
However, this is intentionl. It is a poisonous placeholder value.

I am not sure how to handle `callable()`, `id()`, and `type`.

Logically-null usage cannot be detected, such as in `pypoison.POISON in []` or `True or `.

This module [may cause bugs](https://github.com/bpython/bpython/issues/776)
in your debugger/IDE/editor.  Or at least unexpected behavior.

### Non-serious

The amount of black magic might poison your appreciation of Python.

Python is always nonvenomous; this module makes it poisonous!

## TODOs

* Prevent assignment
* Test
* Tell people about it

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/pypoison/issues/new) or submit PRs.
