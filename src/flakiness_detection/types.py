from __future__ import annotations

from enum import Enum

Success = bool


class Branch(Enum):
    main = "main"
    PR = "PR"
