"""
Shared type definitions for EDA results.

This module defines TypedDict structures used across the EDA pipeline
to standardize how analysis results are represented and passed between
components.
"""

from typing import TypedDict, Union

import pandas as pd


class ResultItem(TypedDict):
    """
    Typed representation of a single EDA result item.

    Attributes:
        id: Unique identifier for the result.
        title: Human-readable title describing the result.
        df: Either a pandas DataFrame containing the result
            or a string representation if tabular data is not applicable.
    """

    id: str
    title: str
    df: Union[pd.DataFrame, str]
