"""
Data type inspection analysis for EDA.

This module provides an analysis implementation that reports the
data types of all columns in a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class DataTypes(AnalysisBase):
    """
    Analysis implementation that reports column data types.

    This analysis returns a tabular representation of each column
    and its corresponding data type.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any):
        """
        Return the data types of all columns in a tabular format.

        Args:
            data: Input pandas DataFrame.
            *args: Unused; included for interface compatibility.

        Returns:
            A pandas DataFrame with column names and their data types.
        """

        series = data.dtypes
        series = series.astype(str)
        df = series.to_frame(name="Value").reset_index()

        return df
