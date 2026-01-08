"""
Streamlit UI utilities for rendering and managing EDA results.

This module provides helper functions to display analysis outputs
and allow users to remove individual results from the UI.
"""

from types import ModuleType
from typing import Sequence

from eda.types import ResultItem


def display(st: ModuleType, results: Sequence[ResultItem]) -> None:
    """
    Render EDA analysis results and allow interactive removal.

    Args:
        st: The Streamlit module instance used to render UI components.
        results: A list of result dictionaries containing display metadata
            and analysis outputs.

    Side Effects:
        - Mutates ``st.session_state.results`` when an entry is deleted.
        - Triggers a Streamlit rerun after deletion.
    """
    ...

    for i, item in enumerate(results):

        with st.container():

            left, right = st.columns([0.85, 0.15])

            with left:

                st.subheader(item["title"])

                st.write(item["df"])

            with right:

                if st.button("Delete", key=item["id"]):

                    st.session_state.results.pop(i)

                    st.rerun()
