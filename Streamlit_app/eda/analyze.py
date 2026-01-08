"""
Analysis dispatcher for exploratory data analysis (EDA).

This module maintains a registry that maps analysis identifiers
to their corresponding EDA analysis implementations and provides
a dispatcher function to execute the selected analysis.

"""

from typing import Any, Dict, Type

import pandas as pd

from eda.analysis_base import AnalysisBase
from eda.analysis_protocol import AnalysisProtocol, AnalysisResult

from .analysis.data_types import DataTypes
from .analysis.describe import Describe
from .analysis.head import Head
from .analysis.mean import Mean
from .analysis.missing import Missing
from .analysis.shape import Shape
from .analysis.unique import Unique
from .analysis.value_counts import ValueCounts

ANALYZE: Dict[str, Type[AnalysisProtocol]] = {
    "preview": Head,
    "mean": Mean,
    "describe": Describe,
    "shape": Shape,
    "data_types": DataTypes,
    "missing_data": Missing,
    "unique": Unique,
    "value_counts": ValueCounts,
}


def analyzer(
    analysis: str, data: pd.DataFrame, n: Any = None
) -> tuple[str, AnalysisResult]:
    """
    Dispatch and execute a selected EDA analysis.

    Args:
        analysis: Identifier of the analysis to run.
        data: Input pandas DataFrame on which the analysis is performed.
        n: Optional parameter required by certain analyses (e.g., row count).

    Returns:
        A tuple containing:
        - The analysis identifier.
        - The result produced by the analysis implementation.

    Raises:
        KeyError: If the analysis identifier is not registered.
        TypeError: If the selected analysis does not inherit from AnalysisBase.
    """

    analysis_cls = ANALYZE[analysis]

    if not issubclass(analysis_cls, AnalysisBase):
        raise TypeError(f"{analysis_cls.__name__} must inherit from AnalysisBase")

    result_df = analysis_cls.compute(data, n)

    title = analysis

    return title, result_df
