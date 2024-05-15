from __future__ import annotations

from enum import Enum

from .flake_detection_db import FlakeDetectionDB
from .test import Test
from .test_report import TestReport


class CategoryReason(Enum):
    # These are PR-relevant
    PASSING = "test is passing in main branch"

    # PR irrelevant statuses
    BROKEN = "broken in main branch"
    FLAKY = "flake seen in main branch"


class TestResultCategorization(dict[CategoryReason, set[Test]]):
    def __missing__(self, key: CategoryReason) -> set[Test]:
        return self.setdefault(key, set())


def flakiness_detection(
    test_history: list[TestReport], test_report: TestReport
) -> TestResultCategorization:

    flake_detection_db = FlakeDetectionDB.build(test_history)

    result = TestResultCategorization()

    for test in test_report:
        if test in flake_detection_db.flakes:
            result[CategoryReason.FLAKY].add(test)

    return result
