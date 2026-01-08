"""
Mean value analysis for EDA.

This module provides an analysis implementation that computes
mean values for numeric columns in a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class Mean(AnalysisBase):
    """
    Analysis implementation that computes column-wise means.

    This analysis calculates the mean for all numeric columns
    in the dataset.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any):
        """
        Compute mean values for numeric columns.

        Args:
            data: Input pandas DataFrame.
            *args: Unused; included for interface compatibility.

        Returns:
            A pandas DataFrame containing mean values for
            numeric columns.
        """

        return data.select_dtypes(include="number").mean().to_frame("Mean")
