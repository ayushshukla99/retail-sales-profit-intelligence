"""
Unit Tests for Business Metrics Engine
======================================
Tests core KPI formulas, safe zero division handling, distinct order counts,
margin calculations, and product rankings.
"""

import numpy as np
import pandas as pd
import pytest
from src.metrics import (
    calculate_kpis,
    aggregate_by_dimension,
    aggregate_time_series,
    get_product_rankings
)


@pytest.fixture
def sample_metrics_df():
    data = {
        "Order ID": ["ORD-1", "ORD-1", "ORD-2", "ORD-3"],
        "Customer ID": ["C1", "C1", "C2", "C3"],
        "Order Date": pd.to_datetime(["2023-01-05", "2023-01-05", "2023-02-10", "2023-03-15"]),
        "Category": ["Technology", "Technology", "Furniture", "Office Supplies"],
        "Sub-Category": ["Phones", "Accessories", "Chairs", "Paper"],
        "Product Name": ["Phone X", "Cable Y", "Chair Z", "Paper Box"],
        "Region": ["East", "East", "West", "Central"],
        "Sales": [1000.0, 200.0, 500.0, 100.0],
        "Profit": [200.0, 50.0, -100.0, 20.0],
        "Quantity": [2, 1, 4, 10],
        "Discount": [0.0, 0.1, 0.4, 0.0]
    }
    return pd.DataFrame(data)


def test_calculate_kpis_basic(sample_metrics_df):
    kpis = calculate_kpis(sample_metrics_df)

    assert kpis["total_sales"] == 1800.0
    assert kpis["total_profit"] == 170.0
    # Profit Margin % = (170 / 1800) * 100 = 9.44%
    assert kpis["profit_margin_pct"] == 9.44
    # Distinct Orders: ORD-1, ORD-2, ORD-3 = 3 orders (not 4 line items!)
    assert kpis["total_orders"] == 3
    assert kpis["total_items"] == 4
    # Units sold = 2 + 1 + 4 + 10 = 17
    assert kpis["units_sold"] == 17
    # Average Order Value = 1800 / 3 = 600.0
    assert kpis["average_order_value"] == 600.0
    # 1 item has profit < 0 (-100.0)
    assert kpis["loss_making_items"] == 1
    assert kpis["loss_total_amount"] == -100.0


def test_calculate_kpis_empty_df():
    empty_df = pd.DataFrame(columns=["Sales", "Profit", "Quantity", "Order ID"])
    kpis = calculate_kpis(empty_df)

    assert kpis["total_sales"] == 0.0
    assert kpis["total_profit"] == 0.0
    assert kpis["profit_margin_pct"] == 0.0
    assert kpis["total_orders"] == 0
    assert kpis["average_order_value"] == 0.0


def test_calculate_kpis_zero_sales():
    df = pd.DataFrame({
        "Order ID": ["O-1"],
        "Sales": [0.0],
        "Profit": [0.0],
        "Quantity": [1],
        "Discount": [0.0]
    })
    kpis = calculate_kpis(df)
    assert kpis["profit_margin_pct"] == 0.0
    assert kpis["average_order_value"] == 0.0


def test_aggregate_by_dimension(sample_metrics_df):
    agg = aggregate_by_dimension(sample_metrics_df, "Category")
    assert len(agg) == 3
    # Check Technology totals
    tech = agg[agg["Category"] == "Technology"].iloc[0]
    assert tech["Sales"] == 1200.0
    assert tech["Profit"] == 250.0
    assert tech["Orders"] == 1  # ORD-1 has both items


def test_get_product_rankings(sample_metrics_df):
    rankings = get_product_rankings(sample_metrics_df, top_n=2)
    top_sales = rankings["top_sales"]
    assert top_sales.iloc[0]["Product Name"] == "Phone X"
    assert top_sales.iloc[0]["Sales"] == 1000.0

    worst_losses = rankings["worst_losses"]
    assert worst_losses.iloc[0]["Product Name"] == "Chair Z"
    assert worst_losses.iloc[0]["Profit"] == -100.0
