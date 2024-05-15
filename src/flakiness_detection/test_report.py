from __future__ import annotations

from collections.abc import Iterable
from typing import NamedTuple

from .test import Test
from .types import Branch
from .types import Success


class TestReport(NamedTuple):
    branch: Branch
    tests: dict[Test, Success]

    @classmethod
    def from_tests(cls, branch: Branch, tests: Iterable[Test]):
        """Run the tests, record results."""
        return cls(branch=branch, tests={test: test() for test in tests})

    # tests: list[Test]
