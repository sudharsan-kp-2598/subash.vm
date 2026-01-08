"""
Dataset shape analysis for EDA.

This module provides an analysis implementation that reports
the shape (rows, columns) of a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class Shape(AnalysisBase):
    """
    Analysis implementation that reports dataset dimensions.

    This analysis returns the number of rows and columns
    in the dataset as a human-readable summary.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any):
        """
        Return the shape of the dataset.

        Args:
            data: Input pandas DataFrame.
            *args: Unused; included for interface compatibility.

        Returns:
            A string describing the number of rows and columns
            in the dataset.
        """

        return f"The shape of the DataFrame is {data.shape}"
