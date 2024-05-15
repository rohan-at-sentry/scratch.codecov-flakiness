from __future__ import annotations

from collections.abc import Iterable
from typing import NamedTuple

from .test import Test
from .types import Success


class TestReport(NamedTuple):
    tests: dict[Test, Success]

    @classmethod
    def from_tests(cls, tests: Iterable[Test]):
        """Run the tests, record results."""
        return cls(tests={test: test() for test in tests})

    # tests: list[Test]
