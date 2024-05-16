from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from hypothesis import assume
from hypothesis import given
from hypothesis import strategies as st

from . import commit


class Name(Enum):
    main = "main"
    PR = "PR"


name_st = st.from_type(Name)


@given(name_st)
def it_is_sometimes_main(branch_name: Name):
    assume(branch_name is Name.main)


@given(name_st)
def it_is_sometimes_PR(branch_name: Name):
    assume(branch_name is Name.PR)


class Commits(NamedTuple):

    branch: Name
    commits: tuple[commit.SHA, ...]


commits_st = st.builds(Commits, name_st, st.lists(commit.SHA_st))


@given(commits_st)
def it_is_has_commits(branch_commits: Commits):
    assume(branch_commits.commits)
