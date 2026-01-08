"""
Descriptive statistics analysis implementation.

This module provides an analysis class that computes summary
statistics for numeric columns in a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class Describe(AnalysisBase):
    """
    Analysis implementation that generates descriptive statistics.

    This analysis computes count, mean, standard deviation,
    minimum, maximum, and quartiles for numeric columns.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any):
        """
        Generate descriptive statistics for the given dataset.

        Args:
            data: Input pandas DataFrame.
            *args: Unused; included for interface compatibility.

        Returns:
            A pandas DataFrame containing descriptive statistics.
        """
        return data.describe()
