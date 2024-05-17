from __future__ import annotations

import heapq

import hypothesis as H

from hypothesis.stateful import consumes
from hypothesis.stateful import Bundle
from hypothesis.stateful import RuleBasedStateMachine
from hypothesis.stateful import initialize
from hypothesis.stateful import rule
from hypothesis.stateful import run_state_machine_as_test  # type:ignore

from .flakiness_detection import flakiness_detection
from .strategies import branch
from .strategies import test
from .strategies.commit import SHA
from .strategies.commit import SHA_st
from .strategies.test_history import TestHistory
from .strategies.test_report import TestReport

HEAP_CAPACITY = 2


BranchCommit = tuple[branch.Name, SHA]


class FlakeEvent(int):
    def __new__(cls, val: int, test_result: test.Result) -> FlakeEvent:
        return super().__new__(cls, val)

    def __init__(self, val: int, test_result: test.Result) -> None:
        super().__init__()
        self.test_result: test.Result = test_result


class FlakinessDetectionStates(RuleBasedStateMachine):
    BranchCommits = Bundle("branch_commits")

    def __init__(self, initial_init=True):
        if initial_init:
            super().__init__()

        # self.current_branch: branch.Name = branch.Name.main
        # self.test_reports: dict[branch.Name, list[TestReport]] = {}
        self.test_history: TestHistory = []
        self.commits_merged: set[SHA] = set()
        self.test_flake_history: dict[test.Name, list[FlakeEvent]] = dict()

        self.should_be_flaky: set[test.Name] = set()

    @initialize()
    def start(self):
        self.__init__(initial_init=False)

    ### def rebase(self): ...
    ### def squash(self): ...
    ### def submit_results(self): ...

    @rule(sha=SHA_st, target=BranchCommits)
    def branch_commit(self, sha: SHA) -> BranchCommit:
        return (branch.Name.PR, sha)

    def update_expectations(self, test_result: test.Result, report_idx: int):
        test_name = test_result.test
        test_state = test_result.state

        # should we add the passed in test result to the list of flakes
        if test_state == test.State.FAIL:
            self.should_be_flaky.add(test_name)

        test_flake_history = self.test_flake_history.setdefault(test_name, [])
        # Pushing the latest test result to the test status history
        heapq.heappush(test_flake_history, FlakeEvent(report_idx, test_result))

        # if the status history is too long, then we pop the earliest test
        if len(test_flake_history) <= HEAP_CAPACITY:
            return
        report_idx = heapq.heappop(test_flake_history)

        # recalculate if there's still a flake afterwards
        if report_idx.test_result.state == test.State.FAIL:
            if all(
                [
                    report_idx.test_result.state == test.State.PASS
                    for report_idx in test_flake_history
                ]
            ):
                # this flake has expired
                self.should_be_flaky.remove(test_name)

    @rule(
        branch_commit=consumes(BranchCommits).filter(
            lambda branch_commit: branch_commit[0] == branch.Name.PR
        ),
        target=BranchCommits,
    )
    def merge(self, branch_commit: BranchCommit) -> BranchCommit:
        _, commit = branch_commit
        H.assume(commit not in self.commits_merged)

        self.commits_merged.add(commit)  # UPDATE commits SET merged=TRUE ...

        for report_idx, report in enumerate(self.test_history):
            if report.commit != commit:
                continue

            for result in report.results:
                if result.state == test.State.FAIL:
                    self.should_be_flaky.add(result.test)
                self.update_expectations(result, report_idx)

        self.check_flakiness()

        return branch.Name.main, commit

    @rule(
        test_name=test.name_st,
        test_state=test.state_st,
        branch_commit=BranchCommits,
    )
    def run_test(
        self,
        test_name: test.Name,
        test_state: test.State,
        branch_commit: BranchCommit,
    ):
        branch_name, commit = branch_commit
        test_result = test.Result(test_name, test_state)
        self.test_history.append(
            TestReport(branch_name, commit, (test_result,))
        )

        # is it relevant
        if branch_name == branch.Name.main or commit in self.commits_merged:
            self.update_expectations(test_result, len(self.test_history) - 1)

        self.check_flakiness()

    def check_flakiness(self):
        flake_report = flakiness_detection(
            self.test_history,
            self.commits_merged,
            flakiness_expiry=HEAP_CAPACITY,
        )

        assert {
            flake.test for flake in flake_report.flaky_tests_in_main
        } == self.should_be_flaky


def it_has_stateful_invariants():
    run_state_machine_as_test(FlakinessDetectionStates, settings=H.settings())


def it_runs_into_this_case():
    state = FlakinessDetectionStates()
    state.start()
    branch_commits_0 = state.branch_commit(sha=SHA.BEEF)
    state.run_test(
        branch_commit=branch_commits_0,
        test_name=test.Name.this_test,
        test_state=test.State.PASS,
    )
    state.run_test(
        branch_commit=branch_commits_0,
        test_name=test.Name.this_test,
        test_state=test.State.PASS,
    )
    state.run_test(
        branch_commit=branch_commits_0,
        test_name=test.Name.this_test,
        test_state=test.State.FAIL,
    )
    branch_commits_1 = state.merge(branch_commit=branch_commits_0)
    state.run_test(
        branch_commit=branch_commits_1,
        test_name=test.Name.this_test,
        test_state=test.State.PASS,
    )
    state.run_test(
        branch_commit=branch_commits_1,
        test_name=test.Name.this_test,
        test_state=test.State.PASS,
    )
    state.teardown()
