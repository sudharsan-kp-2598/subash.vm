"""
PDF export and download utilities for EDA analysis results.

This module provides functionality to generate a password-protected
PDF document from selected EDA results and trigger its download
via the Streamlit interface.
"""

import io
from types import ModuleType
from typing import Any, Dict, List

from reportlab.lib import colors  # type: ignore[import-not-found]
from reportlab.lib.pagesizes import A4  # type: ignore[import-not-found]
from reportlab.lib.pdfencrypt import \
    StandardEncryption  # type: ignore[import-not-found]
from reportlab.lib.styles import \
    getSampleStyleSheet  # type: ignore[import-not-found]
from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)


def generate_pdf(
    results: List[Dict[str, Any]],
    password: str,
    protect: bool,
    st: ModuleType,
) -> None:
    """
    Generate a PDF from selected EDA results and trigger its download.

    Args:
        results: A list of result dictionaries. Each dictionary must contain:
            - ``"title"``: Title of the analysis.
            - ``"df"``: Analysis output as a pandas DataFrame or string.
        password: Password used to encrypt the PDF when protection is enabled.
        protect: Whether to enable PDF password protection.
        st: Streamlit module instance used to trigger the download.

    Side Effects:
        - Creates an in-memory PDF file.
        - Initiates a file download via Streamlit.
    """

    buffer = io.BytesIO()

    encryption = None
    if protect:
        encryption = StandardEncryption(
            userPassword=password,
            ownerPassword=password,
            canPrint=1,
            canModify=0,
            canCopy=0,
            canAnnotate=0,
        )

    doc = SimpleDocTemplate(buffer, pagesize=A4, encrypt=encryption)
    styles = getSampleStyleSheet()

    story: List[Flowable] = []

    for item in results:
        story.append(Paragraph(item["title"], styles["Heading2"]))
        story.append(Spacer(1, 10))

        df = item["df"]

        if isinstance(df, str):
            story.append(Paragraph(df, styles["Normal"]))
            story.append(Spacer(1, 20))
            continue

        data = [df.columns.tolist()] + df.astype(str).values.tolist()

        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ]
            )
        )

        story.append(table)
        story.append(Spacer(1, 20))

    doc.build(story)
    buffer.seek(0)

    st.download_button(
        "Download PDF",
        data=buffer,
        file_name="analysis_results.pdf",
        mime="application/pdf",
    )
