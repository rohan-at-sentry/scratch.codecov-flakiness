from __future__ import annotations

from collections.abc import Callable
from typing import NamedTuple

from .types import Success


class TestResult(NamedTuple):
    test: Test
    result: Success


class Test(NamedTuple):

    func: Callable[[], None]

    @property
    def name(self):
        return self.func.__name__

    def result(self) -> TestResult:
        try:
            self.func()
        except AssertionError:
            return TestResult(self, False)
        else:
            return TestResult(self, True)

    def __call__(self) -> None:
        return self.func()
