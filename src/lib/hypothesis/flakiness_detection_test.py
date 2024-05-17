from __future__ import annotations

from typing import TypeVar

import hypothesis as H
from hypothesis import strategies as st

from .flakiness_detection import flakiness_detection
from .strategies import branch
from .strategies import test
from .strategies.commit import commits_st, Commit, SHA_st
from .strategies.test_report import test_reports_st

# from .strategies.test_history import test_history_st
# from .strategies.test_report import TestReport

T = TypeVar("T")


def list_with_entry(
    draw: st.DrawFn,
    entry: T,
    list_strategy: st.SearchStrategy[list[T]] | None = None,
) -> list[T]:
    if list_strategy is None:
        list_strategy = st.lists(st.from_type(type(entry)))
    result = draw(list_strategy)
    i = draw(st.integers(0, len(result)))
    result.insert(i, entry)
    return result


_commits_st = commits_st()


@st.composite
def test_history_with_failure(
    draw: st.DrawFn,
    failure_branch: branch.Name,
    failure_test: test.Name,
    commits=_commits_st,
    results_strategy: st.SearchStrategy[test.Result] = test.result_st,
):
    failure_result = test.Result(failure_test, test.State.FAIL)

    results = tuple(
        list_with_entry(
            draw, failure_result, list_strategy=st.lists(results_strategy)
        )
    )

    report = draw(
        test_reports_st(
            branch=st.just(failure_branch),
            results=st.just(results),
            commit=commits,
        )
    )
    return list_with_entry(
        draw,
        report,
        list_strategy=st.lists(
            test_reports_st(
                commit=commits, results=st.lists(results_strategy).map(tuple)
            )
        ),
    )


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
        key_sha = data.draw(SHA_st)

        def ensure_not_accepted(commit: Commit) -> Commit:
            if commit.sha == key_sha:
                return commit._replace(pr_accepted=False)
            else:
                return commit

        def ensure_test_name_does_not_fail(result: test.Result) -> test.Result:
            if result.test == test_name:
                return result._replace(state=test.State.PASS)
            else:
                return result

        custom_commits_st = _commits_st.map(ensure_not_accepted)
        custom_results_st = test.result_st.map(ensure_test_name_does_not_fail)

        test_history = data.draw(
            test_history_with_failure(
                failure_branch=branch.Name.PR,
                failure_test=test_name,
                commits=custom_commits_st,
                results_strategy=custom_results_st,
            )
        )

        flake_report = flakiness_detection(test_history)

        assert not any(
            flake.test == test_name
            for flake in flake_report.flaky_tests_in_main
        )
