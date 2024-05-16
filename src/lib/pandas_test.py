from __future__ import annotations

from typing import NamedTuple

import lib.pandas
from pandas import DataFrame


class Point(NamedTuple):
    x: int
    y: int


class Rectangle(NamedTuple):
    top_left: Point
    bottom_right: Point


class DescribeExtractNamedtuples:
    def it_can_explode_a_namedtuple_column(self):
        df = DataFrame({"points": [Point(x=0, y=1), Point(x=11, y=22)]})

        df = lib.pandas.explode_namedtuple(df, "points")

        assert df.columns.to_list() == ["points", "x", "y"]
        assert df.index.to_list() == [0, 1]

        dd: dict[int, dict[str, Point | int]] = df.to_dict(  # type:ignore
            orient="records"
        )
        assert dd == [
            {"points": Point(x=0, y=1), "x": 0, "y": 1},
            {"points": Point(x=11, y=22), "x": 11, "y": 22},
        ]
