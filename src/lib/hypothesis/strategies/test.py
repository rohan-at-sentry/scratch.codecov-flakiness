from __future__ import annotations

from enum import Enum
from typing import NamedTuple

import hypothesis as H
from hypothesis import strategies as st

from . import test  # circular imports, for fun and profit


class Name(Enum):
    this_test = "this_test"
    your_test = "your_test"
    that_test = "that_test"

    def __repr__(self):
        return f"test.Name.{self._value_}"


name_st = st.from_type(Name)


@H.given(name_st)
def it_is_sometimes_this(test_name: Name):
    H.assume(test_name is Name.this_test)
    assert test_name is Name.this_test


@H.given(name_st)
def it_is_sometimes_that(test_name: Name):
    H.assume(test_name is Name.that_test)
    assert test_name is Name.that_test


class State(Enum):
    PASS = "PASS"
    FAIL = "FAIL"

    def __repr__(self):
        return f"test.State.{self._value_}"


state_st = st.from_type(State)


class Result(NamedTuple):
    test: Name
    state: State


result_st = st.from_type(Result)


@H.given(result_st)
def it_sometimes_fails_that_test(test_run: test.Result):
    H.assume(test_run.test == test.Name.this_test)
    H.assume(test_run.state == test.State.FAIL)
