from __future__ import annotations

from enum import Enum
from typing import NamedTuple

import hypothesis as H
from hypothesis import strategies as st

from . import commit


class Name(Enum):
    main = "main"
    PR = "PR"

    def __repr__(self):
        return f"branch.Name.{self._value_}"


name_st = st.from_type(Name)


@H.given(name_st)
def it_is_sometimes_main(branch_name: Name):
    H.assume(branch_name is Name.main)


@H.given(name_st)
def it_is_sometimes_PR(branch_name: Name):
    H.assume(branch_name is Name.PR)


class Commits(NamedTuple):

    branch: Name
    commits: tuple[commit.SHA, ...]


commits_st = st.builds(Commits, name_st, st.lists(commit.SHA_st, unique=True))


@H.given(commits_st)
def it_sometimes_has_a_BAAD_commit(branch_commits: Commits):
    print(branch_commits)
    H.assume(branch_commits.commits)
    H.assume(commit.SHA.BAAD in branch_commits.commits)
