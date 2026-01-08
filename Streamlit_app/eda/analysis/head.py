"""
Preview analysis for EDA.

This module provides an analysis implementation that returns
the first N rows of a pandas DataFrame.
"""

from typing import Any

import pandas as pd

from ..analysis_base import AnalysisBase


class Head(AnalysisBase):
    """
    Analysis implementation that previews dataset rows.

    This analysis returns the first N rows of the dataset
    to provide a quick overview of the data.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any) -> pd.DataFrame:
        """
        Return the first N rows of the dataset.

        Args:
            data: Input pandas DataFrame.
            *args: Optional arguments where the first value specifies
                the number of rows to return.

        Returns:
            A pandas DataFrame containing the first N rows.
        """

        n = args[0] if args else 5
        return data.head(n)
