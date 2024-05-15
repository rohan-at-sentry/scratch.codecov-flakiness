from __future__ import annotations

from ..test import Test


@Test
def passing():
    pass


@Test
def failing():
    raise AssertionError("oh no!")


_fifty_fifty_success = False


@Test
def fifty_fifty():
    global _fifty_fifty_success
    _fifty_fifty_success = not _fifty_fifty_success
    if _fifty_fifty_success:
        pass
    else:
        raise AssertionError("oh no!")
