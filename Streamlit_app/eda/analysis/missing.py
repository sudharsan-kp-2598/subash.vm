"""
Missing value analysis for EDA.

This module provides an analysis implementation that counts
missing (null) values for each column in a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class Missing(AnalysisBase):
    """
    Analysis implementation that counts missing values per column.

    This analysis computes the total number of null entries
    for each column in the dataset.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any):
        """
        Count missing values for each column.

        Args:
            data: Input pandas DataFrame.
            *args: Unused; included for interface compatibility.

        Returns:
            A pandas DataFrame with column names and the count
            of missing values for each column.
        """

        series = data.isna().sum()
        df = series.to_frame(name="Missing").reset_index()

        return df
