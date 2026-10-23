"""
Data Cleaner Module for Retail Sales & Profit Intelligence Platform
===================================================================
Implements an end-to-end, reusable data-cleaning and transformation pipeline.
Detects missing values, duplicates, invalid dates, type anomalies, and numerical
inconsistencies. Generates a comprehensive before-and-after Data Quality Report.
Never modifies the raw input data in-place.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd


@dataclass
class DataQualityReport:
    """Stores detailed metrics and logs from the data cleaning pipeline."""
    raw_row_count: int = 0
    cleaned_row_count: int = 0
    raw_col_count: int = 0
    cleaned_col_count: int = 0
    completely_empty_rows_dropped: int = 0
    duplicate_rows_dropped: int = 0
    missing_key_records_dropped: int = 0
    invalid_dates_handled: int = 0
    negative_shipping_days_adjusted: int = 0
    numeric_type_fixes: List[str] = field(default_factory=list)
    imputed_columns: Dict[str, str] = field(default_factory=dict)
    derived_columns_added: List[str] = field(default_factory=list)
    data_quality_issues: List[str] = field(default_factory=list)
    date_range: Tuple[Optional[str], Optional[str]] = (None, None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to serializable dictionary."""
        return {
            "raw_row_count": self.raw_row_count,
            "cleaned_row_count": self.cleaned_row_count,
            "raw_col_count": self.raw_col_count,
            "cleaned_col_count": self.cleaned_col_count,
            "rows_retained_pct": round((self.cleaned_row_count / max(self.raw_row_count, 1)) * 100, 2),
            "completely_empty_rows_dropped": self.completely_empty_rows_dropped,
            "duplicate_rows_dropped": self.duplicate_rows_dropped,
            "missing_key_records_dropped": self.missing_key_records_dropped,
            "invalid_dates_handled": self.invalid_dates_handled,
            "negative_shipping_days_adjusted": self.negative_shipping_days_adjusted,
            "numeric_type_fixes": self.numeric_type_fixes,
            "imputed_columns": self.imputed_columns,
            "derived_columns_added": self.derived_columns_added,
            "data_quality_issues": self.data_quality_issues,
            "date_range": self.date_range
        }


def clean_retail_data(
    raw_df: pd.DataFrame,
    export_cleaned_path: Optional[Union[str, Path]] = None
) -> Tuple[pd.DataFrame, DataQualityReport]:
    """
    Execute a robust, non-destructive data cleaning and enrichment pipeline.

    Parameters
    ----------
    raw_df : pd.DataFrame
        The raw dataset loaded from CSV or Excel.
    export_cleaned_path : Optional[Union[str, Path]]
        Optional file path to persist the cleaned DataFrame (CSV).

    Returns
    -------
    Tuple[pd.DataFrame, DataQualityReport]
        Cleaned, enriched DataFrame and an audit report of transformations.
    """
    # 1. Non-destructive copy
    df = raw_df.copy()
    report = DataQualityReport()
    report.raw_row_count = len(df)
    report.raw_col_count = len(df.columns)

    # 2. Trim string whitespace from column headers
    df.columns = df.columns.astype(str).str.strip()

    # 3. Detect and remove completely empty rows
    all_null_mask = df.isnull().all(axis=1)
    empty_count = int(all_null_mask.sum())
    if empty_count > 0:
        df = df[~all_null_mask].reset_index(drop=True)
        report.completely_empty_rows_dropped = empty_count
        report.data_quality_issues.append(f"Detected and dropped {empty_count} completely blank rows.")

    # 4. Standardize column names mapping (handle minor naming variations)
    rename_map = {
        "Sub Category": "Sub-Category",
        "Sub_Category": "Sub-Category",
        "Order_Date": "Order Date",
        "Ship_Date": "Ship Date",
        "Ship_Mode": "Ship Mode",
        "Customer_ID": "Customer ID",
        "Customer_Name": "Customer Name",
        "Product_ID": "Product ID",
        "Product_Name": "Product Name",
        "Postal_Code": "Postal Code"
    }
    for old_col, new_col in rename_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)

    # Verify critical columns exist
    critical_cols = ["Sales", "Profit"]
    missing_critical = [col for col in critical_cols if col not in df.columns]
    if missing_critical:
        raise ValueError(f"Uploaded dataset is missing critical monetary columns: {missing_critical}")

    # 5. Handle missing values in essential identifier & monetary columns
    # We require valid Order Date, Sales, and Profit to perform retail intelligence.
    if "Order ID" in df.columns:
        null_order_id = df["Order ID"].isnull()
    else:
        null_order_id = pd.Series(False, index=df.index)

    null_metrics = df["Sales"].isnull() | df["Profit"].isnull()
    unusable_rows = null_order_id | null_metrics
    dropped_unusable = int(unusable_rows.sum())
    if dropped_unusable > 0:
        df = df[~unusable_rows].reset_index(drop=True)
        report.missing_key_records_dropped = dropped_unusable
        report.data_quality_issues.append(
            f"Removed {dropped_unusable} records with missing Order ID, Sales, or Profit."
        )

    # 6. Deduplication (remove exact duplicate records)
    # Note: Retains multiple items in the same Order ID if different products or values.
    # Exclude synthetic auto-increment 'Row ID' when evaluating true duplicates if present.
    eval_cols = [c for c in df.columns if c != "Row ID"]
    exact_dups = int(df.duplicated(subset=eval_cols).sum())
    if exact_dups > 0:
        df = df.drop_duplicates(subset=eval_cols, keep="first").reset_index(drop=True)
        report.duplicate_rows_dropped = exact_dups
        report.data_quality_issues.append(f"Removed {exact_dups} duplicate transaction records.")

    # 7. Convert and validate numeric fields
    numeric_cols = ["Sales", "Profit", "Quantity", "Discount"]
    for col in numeric_cols:
        if col in df.columns:
            orig_dtype = str(df[col].dtype)
            # Remove currency symbols or commas if present as string
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace("$", "", regex=False)
                df[col] = df[col].str.replace(",", "", regex=False).str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")
            if str(df[col].dtype) != orig_dtype:
                report.numeric_type_fixes.append(f"Coerced '{col}' from {orig_dtype} to {df[col].dtype}")

    # Fill any remaining NaNs in numeric columns with reasonable values
    if "Quantity" in df.columns:
        df["Quantity"] = df["Quantity"].fillna(1).clip(lower=1)
        df["Quantity"] = df["Quantity"].round().astype(int)
    if "Discount" in df.columns:
        df["Discount"] = df["Discount"].fillna(0.0).clip(lower=0.0, upper=1.0)
    if "Sales" in df.columns:
        # Sales should be non-negative
        df["Sales"] = df["Sales"].fillna(0.0).clip(lower=0.0)
    if "Profit" in df.columns:
        df["Profit"] = df["Profit"].fillna(0.0)

    # 8. Date Parsing and Validation
    date_cols = ["Order Date", "Ship Date"]
    for col in date_cols:
        if col in df.columns:
            # Using format='mixed' to handle variations like MM/DD/YYYY and YYYY-MM-DD cleanly
            orig_nulls = df[col].isnull().sum()
            df[col] = pd.to_datetime(df[col], format="mixed", errors="coerce")
            new_nulls = df[col].isnull().sum()
            if new_nulls > orig_nulls:
                invalid_dates = int(new_nulls - orig_nulls)
                report.invalid_dates_handled += invalid_dates
                report.data_quality_issues.append(
                    f"Converted unparseable dates in '{col}' ({invalid_dates} rows) to NaT."
                )

    # Drop records where Order Date is missing or invalid
    if "Order Date" in df.columns:
        invalid_order_dates = df["Order Date"].isnull()
        if invalid_order_dates.any():
            invalid_cnt = int(invalid_order_dates.sum())
            df = df[~invalid_order_dates].reset_index(drop=True)
            report.data_quality_issues.append(f"Dropped {invalid_cnt} rows with invalid/missing Order Date.")

    # 9. Handle non-critical missing values (e.g., Postal Code, Region, Category)
    if "Postal Code" in df.columns:
        if df["Postal Code"].isnull().any():
            impute_count = int(df["Postal Code"].isnull().sum())
            df["Postal Code"] = df["Postal Code"].fillna(99999)
            # Format as clean 5-digit string if possible
            df["Postal Code"] = df["Postal Code"].apply(
                lambda x: f"{int(x):05d}" if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
            )
            report.imputed_columns["Postal Code"] = f"Imputed {impute_count} missing postal codes with '99999'."

    categorical_fills = {
        "Region": "Unknown Region",
        "Category": "Uncategorized",
        "Sub-Category": "General",
        "Segment": "Standard",
        "Ship Mode": "Standard Class",
        "Country": "United States",
        "City": "Unknown City",
        "State": "Unknown State"
    }
    for col, default_val in categorical_fills.items():
        if col in df.columns and df[col].isnull().any():
            missing_count = int(df[col].isnull().sum())
            df[col] = df[col].fillna(default_val).astype(str).str.strip()
            report.imputed_columns[col] = f"Imputed {missing_count} missing values with '{default_val}'."

    # 10. Enrich with Derived Business Intelligence Features
    if "Order Date" in df.columns:
        df["Order Year"] = df["Order Date"].dt.year
        df["Order Month"] = df["Order Date"].dt.month
        df["Order YearMonth"] = df["Order Date"].dt.strftime("%Y-%m")
        df["Order Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
        df["Order DayOfWeek"] = df["Order Date"].dt.day_name()
        report.derived_columns_added.extend([
            "Order Year", "Order Month", "Order YearMonth", "Order Quarter", "Order DayOfWeek"
        ])
        min_date = df["Order Date"].min().strftime("%Y-%m-%d") if not df.empty else None
        max_date = df["Order Date"].max().strftime("%Y-%m-%d") if not df.empty else None
        report.date_range = (min_date, max_date)

    if "Order Date" in df.columns and "Ship Date" in df.columns:
        # Calculate shipping duration in days
        df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
        # Validate that shipping duration is non-negative
        negative_ship = df["Shipping Days"] < 0
        if negative_ship.any():
            neg_count = int(negative_ship.sum())
            report.negative_shipping_days_adjusted = neg_count
            report.data_quality_issues.append(
                f"Corrected {neg_count} records where Ship Date was earlier than Order Date."
            )
            df.loc[negative_ship, "Ship Date"] = df.loc[negative_ship, "Order Date"]
            df.loc[negative_ship, "Shipping Days"] = 0
        df["Shipping Days"] = df["Shipping Days"].fillna(0).astype(int)
        report.derived_columns_added.append("Shipping Days")

    # Safe Profit Margin % Calculation at the transaction item level
    # If Sales is 0, Profit Margin % is defined as 0.0% to prevent division by zero
    df["Profit Margin %"] = np.where(
        df["Sales"] > 0,
        (df["Profit"] / df["Sales"]) * 100.0,
        0.0
    ).round(2)
    report.derived_columns_added.append("Profit Margin %")

    # Loss indicator
    df["Is Loss"] = df["Profit"] < 0
    report.derived_columns_added.append("Is Loss")

    # Discount Band categorization
    if "Discount" in df.columns:
        bins = [-0.01, 0.001, 0.20, 0.40, 0.60, 1.01]
        labels = ["0% (No Discount)", "1% - 20%", "21% - 40%", "41% - 60%", "> 60%"]
        df["Discount Band"] = pd.cut(df["Discount"], bins=bins, labels=labels)
        report.derived_columns_added.append("Discount Band")

    # Finalize report metrics
    report.cleaned_row_count = len(df)
    report.cleaned_col_count = len(df.columns)

    # 11. Export cleaned dataset if requested
    if export_cleaned_path:
        out_p = Path(export_cleaned_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_p, index=False, encoding="utf-8")

    return df, report
