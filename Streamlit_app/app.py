"""
Streamlit application entry point for CSV exploratory data analysis.

This module defines the main Streamlit application used to upload
CSV files, run selected EDA analyses, display results, and export
them as a PDF.
"""

import uuid
from types import ModuleType
from typing import List, cast

import pandas as pd
import streamlit as stream  # type: ignore

from eda.analyze import analyzer
from eda.display import display
from eda.saver import saver
from eda.types import ResultItem


def main(st: ModuleType) -> None:
    """
    Run the Streamlit-based CSV exploratory data analysis application.

    Args:
        st: Streamlit module instance used to render the UI.

    Side Effects:
        - Reads uploaded CSV files.
        - Mutates ``st.session_state`` to store analysis results.
        - Renders interactive UI components.
    """

    st.set_page_config(page_title="EDA Analyzer for CSV", layout="wide")

    st.title("EDA Analyzer for CSV")
    st.sidebar.header("Controls")

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=["csv"],
    )

    # -------------------------------------------------
    # Session state initialization (Pylance-safe)
    # -------------------------------------------------

    results = cast(
        List[ResultItem],
        st.session_state.setdefault("results", []),
    )

    if "open_save" not in st.session_state:
        st.session_state.open_save = False

    if uploaded_file is None:
        results.clear()
        st.session_state.open_save = False
        return

    # -------------------------------------------------
    # Data loading
    # -------------------------------------------------
    df = pd.read_csv(uploaded_file)  # type: ignore

    # -------------------------------------------------
    # Analysis selection
    # -------------------------------------------------
    analysis = st.sidebar.selectbox(
        "Analyze",
        options=[
            "preview",
            "mean",
            "describe",
            "shape",
            "data_types",
            "missing_data",
            "unique",
            "value_counts",
        ],
        index=None,
        placeholder="Type to search analysis…",
    )

    preview_rows = None
    selected_column = None

    if analysis == "preview":
        preview_rows = st.sidebar.number_input(
            "Rows to display",
            min_value=1,
            max_value=len(df),
            value=5,
        )

    elif analysis == "value_counts":
        selected_column = st.sidebar.selectbox(
            "Select column",
            options=df.columns,
        )

    # -------------------------------------------------
    # Run analysis
    # -------------------------------------------------
    if st.sidebar.button("Analyze") and analysis:
        st.session_state.open_save = False

        title, result = analyzer(
            analysis=analysis,
            data=df,
            n=preview_rows or selected_column,
        )

        
        results.append(
            {
                "id": str(uuid.uuid4()),
                "title": title,
                "df": result,
            }
        )

    # -------------------------------------------------
    # Save / Display
    # -------------------------------------------------
    _, right = st.columns([0.9, 0.1])

    with right:
        if st.button(
            "Save",
            disabled=not results,
        ):
            st.session_state.open_save = True

    display(st=st, results=results)
    saver(st=st, results=results)


if __name__ == "__main__":
    main(stream)
