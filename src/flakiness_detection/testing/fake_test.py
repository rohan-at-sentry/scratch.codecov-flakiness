from __future__ import annotations

from ..test import Test


@Test
def passing():
    pass


@Test
def failing():
    raise AssertionError("oh no!")


__fifty_fifty_success = False


@Test
def fifty_fifty():
    global __fifty_fifty_success
    __fifty_fifty_success = not __fifty_fifty_success
    if __fifty_fifty_success:
        pass
    else:
        raise AssertionError("oh no!")
