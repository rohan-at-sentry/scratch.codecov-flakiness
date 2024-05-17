from __future__ import annotations

from collections import deque

import hypothesis as H

# from hypothesis.stateful import precondition
from hypothesis.stateful import Bundle
from hypothesis.stateful import RuleBasedStateMachine
from hypothesis.stateful import initialize
from hypothesis.stateful import invariant
from hypothesis.stateful import rule
from hypothesis.stateful import run_state_machine_as_test  # type:ignore

from .flakiness_detection import flakiness_detection
from .strategies import branch
from .strategies import test
from .strategies.commit import SHA
from .strategies.commit import SHA_st
from .strategies.test_history import TestHistory
from .strategies.test_report import TestReport


class FlakinessDetectionStates(RuleBasedStateMachine):
    Commits = Bundle("commits")

    def __init__(self, initial_init=True):
        if initial_init:
            super().__init__()

        # self.current_branch: branch.Name = branch.Name.main
        # self.test_reports: dict[branch.Name, list[TestReport]] = {}
        self.test_history: TestHistory = []
        self.commits_merged: set[SHA] = set()
        self.test_status_history: dict[test.Name, deque[test.State]]

        self.should_be_flaky: set[test.Name] = set()

    @initialize()
    def start(self):
        self.__init__(initial_init=False)

    ### def rebase(self): ...
    ### def squash(self): ...
    ### def submit_results(self): ...

    @rule(sha=SHA_st, target=Commits)
    def commit(self, sha: SHA) -> SHA:
        return sha

    @rule(commit=Commits)
    def merge(self, commit: SHA) -> None:
        self.commits_merged.add(commit)  # UPDATE commits SET merged=TRUE ...

        for report in self.test_history:
            if report.commit != commit:
                continue

            for result in report.results:
                if result.state == test.State.FAIL:
                    self.should_be_flaky.add(result.test)

    @rule(
        branch_name=branch.name_st,
        test_name=test.name_st,
        test_state=test.state_st,
        commit=Commits,
    )
    def run_test(
        self,
        branch_name: branch.Name,
        test_name: test.Name,
        test_state: test.State,
        commit: SHA,
    ):
        test_result = test.Result(test_name, test_state)
        self.test_history.append(
            TestReport(branch_name, commit, (test_result,))
        )

        if (
            branch_name == branch.Name.main or commit in self.commits_merged
        ) and test_state == test.State.FAIL:
            self.should_be_flaky.add(test_name)

    @invariant()
    def check_flakiness(self):
        flake_report = flakiness_detection(
            self.test_history, self.commits_merged, flakiness_expiry=2
        )

        assert {
            flake.test for flake in flake_report.flaky_tests_in_main
        } == self.should_be_flaky


def it_has_stateful_invariants():
    run_state_machine_as_test(FlakinessDetectionStates, settings=H.settings())
