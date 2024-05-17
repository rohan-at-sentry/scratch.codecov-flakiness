from __future__ import annotations

import hypothesis as H
from hypothesis import strategies as st

# from hypothesis.stateful import precondition
from hypothesis.stateful import RuleBasedStateMachine
from hypothesis.stateful import initialize
from hypothesis.stateful import invariant
from hypothesis.stateful import rule
from hypothesis.stateful import run_state_machine_as_test  # type:ignore

from .flakiness_detection import flakiness_detection
from .strategies import branch
from .strategies import test
from .strategies.commit import SHA
from .strategies.commit import Commit
from .strategies.commit import commits_st
from .strategies.test_history import TestHistory
from .strategies.test_report import TestReport


class FlakinessDetectionStates(RuleBasedStateMachine):
    def __init__(self, initial_init=True):
        if initial_init:
            super().__init__()

        # self.current_branch: branch.Name = branch.Name.main
        self.commits: list[Commit] = [Commit(SHA.BAAD, pr_accepted=False)]
        # self.test_reports: dict[branch.Name, list[TestReport]] = {}
        self.test_history: TestHistory = []

        self.should_be_flaky: set[test.Name] = set()

    @initialize()
    def start(self):
        self.__init__(initial_init=False)

    ### @rule()
    ### def submit_results(self): ...

    @rule(commit=commits_st())
    def commit(self, commit: Commit):
        self.commits.append(commit)

    @rule(
        branch_name=branch.name_st,
        test_name=test.name_st,
        test_state=test.state_st,
    )
    def run_test(
        self,
        branch_name: branch.Name,
        test_name: test.Name,
        test_state: test.State,
    ):
        test_result = test.Result(test_name, test_state)
        commit = self.commits[-1]
        self.test_history.append(
            TestReport(branch_name, commit, (test_result,))
        )

        if (
            branch_name == branch.Name.main or commit.pr_accepted
        ) and test_state == test.State.FAIL:
            self.should_be_flaky.add(test_name)

    @invariant()
    def check_flakiness(self):
        flake_report = flakiness_detection(self.test_history)

        assert {
            flake.test for flake in flake_report.flaky_tests_in_main
        } == self.should_be_flaky


def it_has_stateful_invariants():
    run_state_machine_as_test(FlakinessDetectionStates, settings=H.settings())
