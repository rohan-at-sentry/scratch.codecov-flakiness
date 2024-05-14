from __future__ import annotations

from collections.abc import Callable
from typing import NamedTuple

from .types import Success


class Test(NamedTuple):

    func: Callable[[], None]

    @property
    def name(self):
        return self.func.__name__

    def __call__(self) -> Success:
        try:
            self.func()
        except AssertionError:
            return False
        else:
            return True
