"""
Streamlit utilities for exporting EDA analysis results.

This module provides a helper function to render a save dialog
and export selected EDA analysis results as a PDF file.
"""

from types import ModuleType
from typing import Optional, Sequence

from eda.types import ResultItem

from .downloader import generate_pdf


def saver(
    st: ModuleType,
    results: Optional[Sequence[ResultItem]] | None = None,
) -> None:
    """
    Render a dialog for exporting selected EDA analysis results.

    Args:
        st: Streamlit module instance used to render UI components.
        results: Optional list of analysis result dictionaries. Each dictionary
            must contain at least ``"id"`` and ``"title"`` keys.

    Side Effects:
        - Initializes and mutates entries in ``st.session_state``.
        - Displays a modal dialog for selecting and exporting results.
        - Triggers PDF generation and download when confirmed.
    """

    if results is None:
        results = []

    if "open_save" not in st.session_state:
        st.session_state["open_save"] = False

    if "protect" not in st.session_state:
        st.session_state["protect"] = False

    if "selected" not in st.session_state:
        st.session_state["selected"] = []

    if "password" not in st.session_state:
        st.session_state["password"] = ""

    if "confirm_password" not in st.session_state:
        st.session_state["confirm_password"] = ""

    @st.dialog("Save Analysis Results")
    def save_results_dialog() -> None:
        """Render the save-results dialog and handle user interaction."""

        st.write("Select results to export:")

        selected_results = []
        for item in results:
            if st.checkbox(item["title"], key=f"chk_{item['id']}"):
                selected_results.append(item)  # type: ignore[arg-type]

        st.session_state.selected = selected_results

        st.session_state.protect = st.checkbox(
            "Protect PDF with password",
            value=st.session_state.protect,
        )

        if st.session_state.protect:
            st.session_state.password = st.text_input("Password", type="password")
            st.session_state.confirm_password = st.text_input(
                "Confirm Password", type="password"
            )
        else:
            st.session_state.password = ""
            st.session_state.confirm_password = ""

        if st.button("Generate PDF"):
            if not st.session_state.selected:  # type: ignore
                st.error("Select at least one result")
                return

            if st.session_state.protect and (
                not st.session_state.password
                or st.session_state.password != st.session_state.confirm_password
            ):
                st.error("Passwords do not match")
                return

            generate_pdf(
                results=st.session_state.selected,  # type: ignore[arg-type]
                password=str(st.session_state.password),
                protect=st.session_state.protect,
                st=st,
            )

            st.session_state.open_save = False

    if st.session_state.open_save:
        save_results_dialog()
        st.session_state.open_save = False
