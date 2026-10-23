"""
Data Loader Module for Retail Sales & Profit Intelligence Platform
==================================================================
Handles robust ingestion of CSV and Excel files from local disk or
in-memory file upload buffers (e.g., Streamlit file uploader).
Provides metadata extraction and descriptive summaries of ingested datasets.
"""

import io
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union
import pandas as pd


# Expected baseline columns for the retail superstore dataset
EXPECTED_COLUMNS = [
    "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Customer Name", "Segment",
    "Country", "City", "State", "Postal Code", "Region",
    "Product ID", "Category", "Sub-Category", "Product Name",
    "Sales", "Quantity", "Discount", "Profit"
]


def load_dataset(
    file_source: Union[str, Path, io.BytesIO, io.StringIO, Any],
    file_name: Optional[str] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Load a dataset from a file path or in-memory file buffer (CSV or Excel).

    Parameters
    ----------
    file_source : str, Path, or file-like object
        The source of the dataset.
    file_name : Optional[str]
        Explicit filename, used especially when passing in-memory file buffers.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, Any]]
        The loaded raw DataFrame and a metadata dictionary.

    Raises
    ------
    ValueError
        If the file format is unsupported or file cannot be parsed.
    FileNotFoundError
        If a provided file path does not exist.
    """
    detected_name = ""
    is_excel = False

    # Determine file name and format
    if isinstance(file_source, (str, Path)):
        path_obj = Path(file_source)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found at: {file_source}")
        detected_name = path_obj.name
        is_excel = path_obj.suffix.lower() in [".xlsx", ".xls"]
    elif hasattr(file_source, "name"):
        detected_name = getattr(file_source, "name", "uploaded_file")
        is_excel = detected_name.lower().endswith((".xlsx", ".xls"))
    elif file_name:
        detected_name = file_name
        is_excel = detected_name.lower().endswith((".xlsx", ".xls"))
    else:
        detected_name = "in_memory_data.csv"
        is_excel = False

    df: Optional[pd.DataFrame] = None
    last_error: Optional[Exception] = None

    if is_excel:
        try:
            df = pd.read_excel(file_source, engine="openpyxl")
        except Exception as e:
            try:
                # Fallback without engine specification if openpyxl fails for older formats
                df = pd.read_excel(file_source)
            except Exception as inner_e:
                raise ValueError(f"Failed to read Excel file '{detected_name}': {inner_e}") from e
    else:
        # CSV reading with fallback encodings
        encodings_to_try = ["utf-8", "windows-1252", "latin1", "iso-8859-1", "cp1252"]
        for enc in encodings_to_try:
            try:
                if hasattr(file_source, "seek"):
                    file_source.seek(0)
                df = pd.read_csv(file_source, encoding=enc)
                break
            except (UnicodeDecodeError, Exception) as e:
                last_error = e
                continue

        if df is None:
            raise ValueError(
                f"Could not decode CSV file '{detected_name}' using standard encodings "
                f"({', '.join(encodings_to_try)}). Error: {last_error}"
            )

    # Basic metadata extraction
    metadata = {
        "file_name": detected_name,
        "format": "Excel" if is_excel else "CSV",
        "raw_rows": len(df),
        "raw_columns": len(df.columns),
        "memory_mb": float(round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)),
        "columns": df.columns.tolist(),
        "has_expected_columns": all(col in df.columns for col in ["Sales", "Profit", "Order Date"])
    }

    return df, metadata


def inspect_raw_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Inspect the raw DataFrame and return summary diagnostics before cleaning.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset.

    Returns
    -------
    Dict[str, Any]
        Dictionary with diagnostic metrics (shape, nulls, duplicates, column types).
    """
    total_rows = len(df)
    null_counts = df.isnull().sum()
    null_pct = (null_counts / max(total_rows, 1) * 100).round(2)

    null_summary = {
        col: {"count": int(null_counts[col]), "percentage": float(null_pct[col])}
        for col in df.columns if null_counts[col] > 0
    }

    duplicate_rows = int(df.duplicated().sum())

    # Detect completely empty rows
    completely_empty_rows = int(df.isnull().all(axis=1).sum())

    return {
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "duplicate_rows": duplicate_rows,
        "completely_empty_rows": completely_empty_rows,
        "columns_with_nulls": len(null_summary),
        "null_details": null_summary,
        "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
