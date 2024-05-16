from __future__ import annotations

import hypothesis as H
from hypothesis import strategies as st

from .test_report import TestReport

TestHistory = list[TestReport]


test_history_st = st.from_type(TestHistory)


@H.given(test_history_st)
def it_sometimes_is_just_one_report(test_history: TestHistory):
    if test_history:
        assert isinstance(test_history[0], TestReport)
