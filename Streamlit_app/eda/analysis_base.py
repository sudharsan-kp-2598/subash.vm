"""
Abstract base definitions for exploratory data analysis (EDA) components.

This module defines the common interface that all EDA analysis
implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Any, Union

import pandas as pd

AnalysisResult = Union[pd.DataFrame, str]


class AnalysisBase(ABC):
    """
    Abstract base class for all EDA analysis implementations.

    Subclasses must implement the `compute` method to perform
    a specific analysis on a pandas DataFrame and return a result
    without mutating the input data.
    """

    @classmethod
    @abstractmethod
    def compute(cls, data: pd.DataFrame, *args: Any) -> AnalysisResult:
        """
        Compute an analysis result from the input dataset.

        Args:
            data: Input pandas DataFrame to analyze.
            *args: Optional arguments required by the specific analysis.

        Returns:
            The analysis result, typically a DataFrame or a string summary.
        """

        raise NotImplementedError
