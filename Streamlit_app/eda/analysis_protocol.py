"""
Protocol defining the interface for exploratory data analysis (EDA) analysis classes.

This module declares a structural typing contract that analysis implementations
must satisfy in order to be compatible with the EDA framework.
"""

from typing import Any, Protocol, Union

import pandas as pd

AnalysisResult = Union[pd.DataFrame, str]


class AnalysisProtocol(Protocol):
    """
    Structural typing protocol for EDA analysis implementations.

    Any class conforming to this protocol must provide a `compute` class
    method with the specified signature.
    """

    @classmethod
    def compute(cls, data: pd.DataFrame, *args: Any) -> AnalysisResult:
        """
        Compute an analysis result from the given dataset.

        Args:
            data: Input pandas DataFrame to analyze.
            *args: Additional arguments required by the concrete analysis.

        Returns:
            The analysis result produced by the implementation.
        """
        ...
