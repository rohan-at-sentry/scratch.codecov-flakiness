#!/usr/bin/env pytest
from __future__ import annotations

from ..flakiness_detection import flakiness_detection
from ..test_report import TestReport
from ..testing import fake_test
from ..types import Branch

TESTS = (fake_test.fifty_fifty, fake_test.failing, fake_test.passing)

PR_HISTORY: list[TestReport] = [
    TestReport.from_tests(branch=Branch.PR, tests=TESTS) for _ in range(10)
]


class DescribeBasicFlakinessDetection:
    def it_detects_a_50_50_flake(self):
        tests = [fake_test.fifty_fifty]

        test_results = TestReport.from_tests(Branch.PR, tests)
        flakes = flakiness_detection(PR_HISTORY, test_results)
        assert list(flakes) == [fake_test.fifty_fifty]

    def it_never_detects_passing_test(self):
        tests = [fake_test.passing]

        test_results = TestReport.from_tests(Branch.PR, tests)
        flakes = flakiness_detection(PR_HISTORY, test_results)
        assert list(flakes) == []

    def it_never_detects_failing_test(self):
        tests = [fake_test.failing]

        test_results = TestReport.from_tests(Branch.PR, tests)
        flakes = flakiness_detection(PR_HISTORY, test_results)
        assert list(flakes) == []


class DescribeBranchBehavior:
    """
    The system uses the concept of "main branch" versus "feature branch" to do
    more advanced analyses.
    """

    def it_discounts_failures_broken_in_main(self):
        """
        A test that's broken in main is not relevant to merging the current PR,
        and so should not be counted as a relevant-and-failing test.
        """

    def it_discounts_flakes_seen_in_main(self):
        """
        A test that's (currently!) flaky in main is similarly not relevant.
        """

    def it_counts_failures_not_seen_in_main(self):
        """
        Any failure that has never appeared in main is PR-relevant.
        """

    def it_disregards_broken_pr_tests(self):
        """"""


class DescribeErrorDifferentiation:
    """
    The system can distinguish between "same" and "different" failures.
    """


class DescribeCurrentlyFlakyDetection:
    """
    The system can determine when flaky periods started and ended.
    """

    def it_counts_failures_that_were_flaky_then_fixed(self):
        """
        If we fix flakiness then that failure reappears in our PR, it should
        be marked as pr-relevant.

        e.g.
            * test was 50% flaky for one week six months ago
            * we're seeing that same failure in our branch, today
        """
