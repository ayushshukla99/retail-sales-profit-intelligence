"""
Unit Tests for Exploratory Data Analysis & Insights
===================================================
Tests descriptive statistics, IQR outlier detection, reproducible sampling,
and algorithmic business insights generation.
"""

import numpy as np
import pandas as pd
import pytest
from src.eda import (
    get_dataset_overview,
    get_descriptive_statistics,
    detect_outliers_iqr,
    get_sampling_subsets
)
from src.insights import generate_business_insights
from src.metrics import calculate_kpis


@pytest.fixture
def sample_eda_df():
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        "Order ID": [f"ORD-{i}" for i in range(n)],
        "Order Date": pd.date_range("2023-01-01", periods=n, freq="D"),
        "Category": np.random.choice(["Technology", "Furniture", "Office Supplies"], size=n),
        "Sub-Category": np.random.choice(["Phones", "Chairs", "Paper", "Tables"], size=n),
        "Region": np.random.choice(["East", "West", "Central", "South"], size=n),
        "Segment": np.random.choice(["Consumer", "Corporate", "Home Office"], size=n),
        "Sales": np.random.exponential(scale=200, size=n) + 10,
        "Profit": np.random.normal(loc=30, scale=80, size=n),
        "Quantity": np.random.randint(1, 10, size=n),
        "Discount": np.random.choice([0.0, 0.1, 0.2, 0.5, 0.7], size=n)
    })


def test_get_dataset_overview(sample_eda_df):
    overview = get_dataset_overview(sample_eda_df)
    assert overview["total_rows"] == 100
    assert overview["total_columns"] == 10
    assert not overview["columns_summary"].empty


def test_get_descriptive_statistics(sample_eda_df):
    stats = get_descriptive_statistics(sample_eda_df)
    assert len(stats) == 4  # Sales, Profit, Quantity, Discount
    cols = stats["Metric Column"].tolist()
    assert "Sales" in cols
    assert "Profit" in cols


def test_detect_outliers_iqr(sample_eda_df):
    outliers = detect_outliers_iqr(sample_eda_df)
    assert "Sales" in outliers
    assert "q1" in outliers["Sales"]
    assert "q3" in outliers["Sales"]
    assert "iqr" in outliers["Sales"]
    assert outliers["Sales"]["lower_fence"] <= outliers["Sales"]["upper_fence"]


def test_get_sampling_subsets_reproducibility(sample_eda_df):
    sample1 = get_sampling_subsets(sample_eda_df, sample_size=20, random_seed=42)
    sample2 = get_sampling_subsets(sample_eda_df, sample_size=20, random_seed=42)

    pd.testing.assert_frame_equal(sample1["random_sample"], sample2["random_sample"])
    pd.testing.assert_frame_equal(sample1["stratified_sample"], sample2["stratified_sample"])


def test_generate_business_insights(sample_eda_df):
    kpis = calculate_kpis(sample_eda_df)
    insights = generate_business_insights(sample_eda_df, kpis)

    assert isinstance(insights, list)
    assert len(insights) > 0
    for item in insights:
        assert "title" in item
        assert "finding" in item
        assert "supporting_metric" in item
        assert "recommendation" in item
