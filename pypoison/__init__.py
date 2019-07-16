# Copyright (c) 2019, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.
"""Nothing says "DO NOT USE" like a poison value.

Sometimes you need a value to represent absence of a value.
However, sometimes you want to make absolutely sure this value is not used in any way, shape, form, or anything whatsoever.
In these cases, values like `None`, `float('NaN')`, or `False` don't really fit, because you can still "touch" these values.

That's what poison values are for.
Because nothing says "DO NOT USE" like a poison value.

This module provides an object that overrides all methods to raise an exception.
"""

from ._impl import get_poison, set_exception, set_handler
