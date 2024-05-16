from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Iterator
from typing import NamedTuple

from .test import Test
from .test import TestResult
from .types import Branch


class TestReport(NamedTuple):
    """This represents users' input: a json report of test failures."""

    branch: Branch
    results: tuple[TestResult, ...]

    @classmethod
    def from_tests(cls, branch: Branch, tests: Iterable[Test]):
        """Run the tests, record results."""
        return cls(
            branch=branch, results=tuple(test.result() for test in tests)
        )

    def __iter__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
    ) -> Iterator[Test]:
        for test, success in self.results:
            del success
            yield test
