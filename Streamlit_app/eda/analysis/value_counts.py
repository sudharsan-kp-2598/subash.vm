"""
Value frequency analysis for EDA.

This module provides an analysis implementation that computes
frequency counts for values in a specified column of a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class ValueCounts(AnalysisBase):
    """
    Analysis implementation that computes value frequencies.

    This analysis calculates how often each distinct value
    appears in a specified column.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any):
        """
        Compute value counts for a specified column.

        Args:
            data: Input pandas DataFrame.
            *args: Optional arguments where the first value specifies
                the column name for which value counts are computed.

        Returns:
            A pandas DataFrame with unique values and their
            corresponding frequency counts.

        Raises:
            KeyError: If the specified column does not exist.
        """

        column = args[0] if args else None
        s = data[column].value_counts()
        df = s.to_frame(name="Count").reset_index()

        return df
