from __future__ import annotations

from typing import NamedTuple

from hypothesis import strategies as st

from . import branch
from . import test
from .commit import SHA
from .commit import SHA_st


class TestReport(NamedTuple):
    branch: branch.Name
    commit: SHA

    results: tuple[test.Result, ...]


results_st = st.lists(test.result_st).map(tuple)


@st.composite
def test_reports_st(
    draw: st.DrawFn, branch=branch.name_st, commit=SHA_st, results=results_st
):

    return TestReport(draw(branch), draw(commit), draw(results))
