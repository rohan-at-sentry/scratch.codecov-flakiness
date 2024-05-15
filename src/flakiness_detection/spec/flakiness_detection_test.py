#!/usr/bin/env pytest
from __future__ import annotations

from ..flakiness_detection import flakiness_detection
from ..test_report import TestReport
from ..testing import fake_test

TEST_HISTORY: list[TestReport] = []

TESTS = (fake_test.fifty_fifty, fake_test.failing, fake_test.passing)

for _ in range(10):
    TEST_HISTORY.append(TestReport.from_tests(tests=TESTS))


class DescribeFlakinessDetection:
    def it_detects_a_50_50_flake(self):
        tests = [fake_test.fifty_fifty]

        test_results = TestReport.from_tests(tests)
        flakes = flakiness_detection(TEST_HISTORY, test_results)
        assert list(flakes) == [fake_test.fifty_fifty]

    def it_never_detects_passing_test(self):
        tests = [fake_test.passing]

        test_results = TestReport.from_tests(tests)
        flakes = flakiness_detection(TEST_HISTORY, test_results)
        assert list(flakes) == []

    def it_never_detects_failing_test(self):
        tests = [fake_test.failing]

        test_results = TestReport.from_tests(tests)
        flakes = flakiness_detection(TEST_HISTORY, test_results)
        assert list(flakes) == []


class DescribeBranchBehavior:
    def it_discounts_tests_broken_in_main(self):
        """
        A test that's broken in main is not relevant to merging the current PR,
        and so should not be counted as a relevant-and-failing test.
        """
        ...


class DescribeHistoryBehavior:
    def it_never_detects_a_passing_test_even_if_it_was_previously_a_flake(
        self,
    ):
        """ """
        ...
