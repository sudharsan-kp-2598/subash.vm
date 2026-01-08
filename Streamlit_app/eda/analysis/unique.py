"""
Unique value analysis for EDA.

This module provides an analysis implementation that counts
the number of distinct values in each column of a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class Unique(AnalysisBase):
    """
    Analysis implementation that counts unique values per column.

    This analysis computes the number of distinct (non-null)
    values for each column in the dataset.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any):
        """
        Count unique values for each column.

        Args:
            data: Input pandas DataFrame.
            *args: Unused; included for interface compatibility.

        Returns:
            A pandas DataFrame with column names and the count
            of unique values for each column.
        """

        series = data.nunique()
        df = series.to_frame(name="Value").reset_index()

        return df
