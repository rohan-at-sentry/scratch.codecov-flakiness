from __future__ import annotations

from typing import TypeVar

import hypothesis as H
from hypothesis import strategies as st

from .flakiness_detection import flakiness_detection
from .strategies import branch
from .strategies import test
from .strategies.commit import commits_st
from .strategies.test_report import test_reports_st

# from .strategies.test_history import test_history_st
# from .strategies.test_report import TestReport

T = TypeVar("T")


def list_with_entry(draw: st.DrawFn, entry: T) -> list[T]:
    result = draw(st.lists(st.from_type(type(entry))))
    i = draw(st.integers(0, len(result)))
    result.insert(i, entry)
    return result


@st.composite
def test_history_with_failure(
    draw: st.DrawFn,
    failure_branch: branch.Name,
    failure_test: test.Name,
    commits=commits_st(),
):
    failure_result = test.Result(failure_test, test.State.FAIL)

    results = tuple(list_with_entry(draw, failure_result))
    report = draw(
        test_reports_st(
            branch=st.just(failure_branch),
            results=st.just(results),
            commit=commits,
        )
    )
    return list_with_entry(draw, report)


class DescribeFlakinessDetection:

    @H.given(st.data())
    def it_will_report_any_failure_on_main_branch(self, data: st.DataObject):
        test_name = data.draw(test.name_st)
        test_history = data.draw(
            test_history_with_failure(
                failure_branch=branch.Name.main, failure_test=test_name
            )
        )

        flake_report = flakiness_detection(test_history)

        assert any(
            flake.test == test_name
            for flake in flake_report.flaky_tests_in_main
        )

    @H.given(st.data())
    def it_will_not_report_failure_on_unaccepted_pr_commit(
        self, data: st.DataObject
    ):
        test_name = data.draw(test.name_st)

        test_history = data.draw(
            test_history_with_failure(
                failure_branch=branch.Name.PR,
                failure_test=test_name,
                commits=commits_st(pr_accepted=st.just(False)),
            )
        )

        flake_report = flakiness_detection(test_history)

        assert any(
            flake.test == test_name
            for flake in flake_report.flaky_tests_in_main
        )
