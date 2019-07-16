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

Just use the value returned by `pypoison.get_poison()` when you need a poison value.

The object is always the same object.

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
>>> 1 in pypoison.get_poison()
ValueError: Tried to access __contains__ on poison value.
>>> pypoison.get_poison() / 1
ValueError: Tried to access __truediv__ on poison value.
>>> 1 + Foo()
ValueError: Tried to access __radd__ on poison value.
>>> pypoison.get_poison() * 4
ValueError: Tried to access __mul__ on poison value.
>>> pypoison.get_poison() % 3
ValueError: Tried to access __mod__ on poison value.
>>> 3 % pypoison.get_poison()
ValueError: Tried to access __rmod__ on poison value.
>>> '{}'.format(pypoison.get_poison())
ValueError: Tried to access __format__ on poison value.
>>> '{!r}'.format(pypoison.get_poison())
ValueError: Tried to access __repr__ on poison value.
>>> list(pypoison.get_poison())
ValueError: Tried to access __iter__ on poison value.
>>> help(pypoison.get_poison())
ValueError: Tried to access __getattribute__ on poison value.
>>> pypoison.get_poison() == 42
ValueError: Tried to access __eq__ on poison value.
```

## Caveat

### Serious

Heavy use of the `inspect` module might fiddle around with the poison object,
however safeguards are in place to make sure that this is not easy.

Passive use, such as `is` or storing it in a passive container (e.g. a list)
cannot be prevented.  However, this is intentionl. This module wants to
provide a poisonous placeholder value, and not an actively malicious value.

I am not sure how to handle `callable()`, `id()`, and `type()`.

Logically-null usage cannot be detected, such as in `pypoison.get_poison() in []`
or `True or pypoison.get_poison()` or even `max([pypoison.get_poison()])`.

This module [may cause bugs](https://github.com/bpython/bpython/issues/776)
in your debugger/IDE/editor.  Or at least unexpected behavior.

Do not store the poison value in a global.  Many tools, e.g. unittest,
walk the global variables and inspect them.

### Non-serious

The amount of black magic might *poison* your appreciation of Python.

Pythonidae are always *[nonvenomous](https://en.wikipedia.org/wiki/Pythonidae)*; this module makes it *poisonous*!

## TODOs

* Do weird stuff with it

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/pypoison/issues/new) or submit PRs.
