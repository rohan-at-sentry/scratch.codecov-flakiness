from __future__ import annotations

from datetime import datetime
from typing import NamedTuple

from .flake import Flake
from .strategies import branch
from .strategies import test
from .strategies.commit import SHA
from .strategies.test_history import TestHistory


class InterestingStuff(NamedTuple):
    flaky_tests_in_main: frozenset[Flake]

    # for later:
    # tests_to_run: ...
    # irrelevant_failures: why


def flakiness_detection(
    # test_report: TestReport,  # for later
    test_history: TestHistory,
    commits_merged: set[SHA],
) -> InterestingStuff:
    """
    Given a user's test report plus the historical data of tests from the same
    repo (the same PR and main branch), we can tell the user some interesting
    stuff.
    """
    flaky_tests_in_main: set[Flake] = set()

    for report in test_history:
        if not (
            report.branch == branch.Name.main
            or report.commit in commits_merged
        ):
            continue  # this report is main-irrelevant

        for result in report.results:
            if result.state == test.State.FAIL:
                flaky_tests_in_main.add(
                    Flake(
                        test=result.test,
                        flakiness=0,
                        first_seen=datetime(1, 1, 1),
                        last_seen=datetime(1, 1, 1),
                        expired=True,
                    )
                )

    return InterestingStuff(frozenset(flaky_tests_in_main))
