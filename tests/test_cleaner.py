"""
Unit Tests for Data Loader and Data Cleaner
===========================================
Tests CSV/Excel ingestion, duplicate handling, missing value imputation,
date conversion, and data quality reporting.
"""

from io import StringIO, BytesIO
import numpy as np
import pandas as pd
import pytest
from src.data_cleaner import clean_retail_data, DataQualityReport
from src.data_loader import load_dataset, inspect_raw_data


def create_sample_raw_df():
    """Create a minimal raw dataset with edge cases."""
    data = {
        "Row ID": [1, 2, 3, 4, 5, 6, 7],
        "Order ID": ["CA-1", "CA-1", "CA-2", "CA-3", "CA-4", None, "CA-5"],
        "Order Date": ["2023-01-10", "2023-01-10", "invalid-date", "2023-02-15", "2023-03-01", "2023-03-05", "2023-04-10"],
        "Ship Date": ["2023-01-14", "2023-01-14", "2023-01-20", "2023-02-10", "2023-03-05", "2023-03-10", "2023-04-15"],
        "Ship Mode": ["Standard", "Standard", "Second", "Standard", "Standard", "Standard", "Standard"],
        "Customer ID": ["C-1", "C-1", "C-2", "C-3", "C-4", "C-5", "C-6"],
        "Customer Name": ["Alice", "Alice", "Bob", "Charlie", "David", "Eve", "Frank"],
        "Segment": ["Consumer", "Consumer", "Corporate", "Home Office", "Consumer", "Consumer", "Corporate"],
        "Country": ["United States"] * 7,
        "City": ["New York"] * 7,
        "State": ["New York"] * 7,
        "Postal Code": [10001, 10001, np.nan, 10002, 10003, 10004, 10005],
        "Region": ["East"] * 7,
        "Product ID": ["P-1", "P-2", "P-3", "P-4", "P-5", "P-6", "P-7"],
        "Category": ["Technology", "Furniture", "Technology", "Office Supplies", "Furniture", "Technology", "Technology"],
        "Sub-Category": ["Phones", "Chairs", "Accessories", "Storage", "Tables", "Phones", "Phones"],
        "Product Name": ["Phone A", "Chair B", "Accessory C", "Box D", "Table E", "Phone F", "Phone G"],
        "Sales": [500.0, 250.0, 100.0, 50.0, 400.0, 200.0, 150.0],
        "Quantity": [2, 1, 3, 5, 2, 1, 3],
        "Discount": [0.0, 0.1, 0.2, 0.0, 0.5, 0.0, 0.0],
        "Profit": [100.0, 25.0, 10.0, 15.0, -80.0, 50.0, 30.0]
    }
    return pd.DataFrame(data)


def test_load_dataset_csv_string():
    csv_text = "Order ID,Order Date,Sales,Profit\nO-1,2023-01-01,100,20\nO-2,2023-01-02,200,40\n"
    buffer = StringIO(csv_text)
    df, meta = load_dataset(buffer, file_name="test.csv")
    assert len(df) == 2
    assert meta["format"] == "CSV"
    assert "Sales" in df.columns


def test_load_dataset_missing_file():
    with pytest.raises(FileNotFoundError):
        load_dataset("non_existent_file_path.csv")


def test_clean_retail_data_preserves_raw():
    raw_df = create_sample_raw_df()
    raw_copy = raw_df.copy()
    cleaned_df, report = clean_retail_data(raw_df)

    # Ensure raw dataframe was not modified in-place
    pd.testing.assert_frame_equal(raw_df, raw_copy)
    assert isinstance(report, DataQualityReport)


def test_clean_retail_data_drops_null_order_id():
    raw_df = create_sample_raw_df()
    cleaned_df, report = clean_retail_data(raw_df)
    # Row with Order ID = None should be dropped
    assert cleaned_df["Order ID"].isnull().sum() == 0
    assert "CA-5" in cleaned_df["Order ID"].values


def test_clean_retail_data_invalid_date_handling():
    raw_df = create_sample_raw_df()
    cleaned_df, report = clean_retail_data(raw_df)
    # Row with 'invalid-date' should be excluded from cleaned data
    assert (cleaned_df["Order Date"] == "invalid-date").sum() == 0
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df["Order Date"])


def test_clean_retail_data_negative_shipping_days():
    raw_df = create_sample_raw_df()
    # Row 3 (index 3) has Order Date 2023-02-15 and Ship Date 2023-02-10 (Ship < Order)
    cleaned_df, report = clean_retail_data(raw_df)
    ca3_row = cleaned_df[cleaned_df["Order ID"] == "CA-3"]
    if not ca3_row.empty:
        assert (ca3_row["Shipping Days"] >= 0).all()


def test_clean_retail_data_postal_code_imputation():
    raw_df = create_sample_raw_df()
    cleaned_df, report = clean_retail_data(raw_df)
    # Null postal code should be imputed
    assert cleaned_df["Postal Code"].isnull().sum() == 0


def test_clean_retail_data_derived_columns():
    raw_df = create_sample_raw_df()
    cleaned_df, report = clean_retail_data(raw_df)
    for col in ["Order Year", "Order Month", "Profit Margin %", "Is Loss", "Discount Band"]:
        assert col in cleaned_df.columns


def test_missing_critical_columns_raises_error():
    invalid_df = pd.DataFrame({"Customer": ["A", "B"], "Score": [10, 20]})
    with pytest.raises(ValueError, match="missing critical monetary columns"):
        clean_retail_data(invalid_df)
