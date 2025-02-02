from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from typing import NamedTuple

from .test import Test
from .test_report import TestReport


@dataclass(frozen=False)
class TestAnalysis:
    ran: int
    failed: int

    def is_flaky(self):
        return 0 < self.failure_rate < 1

    @property
    def failure_rate(self) -> Fraction:
        return Fraction(self.failed, self.ran)


class FlakeDetectionDB(NamedTuple):
    flakes: set[Test]

    @classmethod
    def build(cls, test_history: Iterable[TestReport]):
        db: dict[Test, TestAnalysis] = {}

        for test_report in test_history:
            for test, success in test_report.results:

                if test in db:
                    analysis = db[test]
                else:
                    analysis = db[test] = TestAnalysis(0, 0)

                analysis.ran += 1
                analysis.failed += 0 if success else 1

        return cls(
            flakes={
                test for test, analysis in db.items() if analysis.is_flaky()
            }
        )
