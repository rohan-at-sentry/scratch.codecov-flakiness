from __future__ import annotations

from enum import IntEnum
from typing import NamedTuple

from hypothesis import strategies as st


class SHA(IntEnum):
    BEEF = 0xBEEF
    BAAD = 0xBAAD
    C0DE = 0xC0DE
    # if we need more: C0C0 CAFE DADA FACE F00D FEED

    def __repr__(self):
        return f"commit.SHA.{self:X}"


SHA_st = st.from_type(SHA)
booleans_st = st.booleans()


class Commit(NamedTuple):
    sha: SHA

    # this is the "tip" sha of a PR that was merged/rebased to main
    pr_accepted: bool


@st.composite
def commits_st(draw: st.DrawFn, sha=SHA_st, pr_accepted=booleans_st):
    return Commit(draw(sha), draw(pr_accepted))
