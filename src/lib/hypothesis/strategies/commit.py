from __future__ import annotations

from hypothesis import strategies as st


class SHA(int):
    pass

    def __str__(self):
        return hex(self).upper()

    def __repr__(self):
        return f"SHA({self})"


A12 = SHA(0xA12)
B34 = SHA(0xB34)
C56 = SHA(0xC56)


SHA_st = st.sampled_from((A12, B34, C56))
