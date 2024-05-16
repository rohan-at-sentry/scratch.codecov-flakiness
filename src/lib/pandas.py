from __future__ import annotations

import pandas as pd
from pandas import DataFrame
from pandas import Series


def explode_namedtuple(
    df: DataFrame, column: str, new_name: str | None = None
) -> DataFrame:
    """
    Extract fields from namedtuples in a DataFrame column and add them as new
    columns.
    """
    column_data = df[column]  # type:ignore
    assert isinstance(column_data, Series)

    # Extract fields from the namedtuples
    column_list = column_data.tolist()  # type: ignore

    exploded = DataFrame(column_list, index=df.index)

    # Concatenate the new columns with the original DataFrame
    df = pd.concat([df, exploded], axis=1)

    if new_name is not None:
        df = df.rename(columns={column: new_name})

    return df
