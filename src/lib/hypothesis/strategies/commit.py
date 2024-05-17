from __future__ import annotations

from enum import IntEnum

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
