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
from .strategies.test_history import TestHistory
from .strategies.test_report import TestReport


class FlakinessDetectionStates(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()

        self.current_branch: branch.Name = branch.Name.main
        self.commits: list[Commit] = [Commit(SHA.BAAD, pr_accepted=False)]
        # self.test_reports: dict[branch.Name, list[TestReport]] = {}
        self.test_history: TestHistory = []

        self.should_be_flaky = set(test.Name)

    @initialize()
    def start(self):
        self.current_branch: branch.Name = branch.Name.main
        self.commits: list[Commit] = [Commit(SHA.BAAD, pr_accepted=False)]
        # self.test_reports: dict[branch.Name, list[TestReport]] = {}
        self.test_history: TestHistory = []

        self.should_be_flaky: set[test.Name] = set()

    ### @rule()
    ### def submit_results(self): ...

    @rule(data=st.data(), test_name=test.name_st)
    def run_test(self, data: st.DataObject, test_name: test.Name):
        test_state = data.draw(test.state_st)
        test_result = test.Result(test_name, test_state)
        self.test_history.append(
            TestReport(self.current_branch, self.commits[-1], (test_result,))
        )

        if test_state == test.State.FAIL:
            self.should_be_flaky.add(test_name)

    @invariant()
    def check_flakiness(self):
        flake_report = flakiness_detection(self.test_history)

        assert {
            flake.test for flake in flake_report.flaky_tests_in_main
        } == self.should_be_flaky


def it_has_stateful_invariants():
    run_state_machine_as_test(FlakinessDetectionStates, settings=H.settings())
