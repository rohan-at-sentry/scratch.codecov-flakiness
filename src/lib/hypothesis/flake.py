from __future__ import annotations

from datetime import datetime
from typing import NamedTuple

from .strategies import test


class Flake(NamedTuple):
    test: test.Name
    flakiness: float
    first_seen: datetime
    last_seen: datetime
    expired: bool
