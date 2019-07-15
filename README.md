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
- [TODOs](#todos)
- [Contribute](#contribute)

## Install

Just `pip install pypoison`.

There are no dependencies.

## Usage

Just use the value `pypoison.POISON` when you need a poison value.

If you really must, you can call `pypoison.make_poison(my_exception)`
to get a poison value that raises the object `my_exception`
whenever anything is done with the poison value.

For extra fanciness, you can call `pypoison.make_poison(my_fn)`,
and the poison value will raise whatever `my_fn(method_name)` returns.

## TODOs

* Implement

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/pypoison/issues/new) or submit PRs.
