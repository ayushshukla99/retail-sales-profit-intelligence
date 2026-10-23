"""
Business Metrics Engine for Retail Sales & Profit Intelligence Platform
========================================================================
Implements precise, verified formulas for executive KPIs and segment aggregations.
Guarantees defensive division-by-zero protection, distinct order count enforcement,
and consistent formatting across dashboard and exports.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate top-level executive business performance indicators.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered or full cleaned retail transactions DataFrame.

    Returns
    -------
    Dict[str, Any]
        Dictionary of formatted and raw KPI values.
    """
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "profit_margin_pct": 0.0,
            "total_orders": 0,
            "total_items": 0,
            "units_sold": 0,
            "average_order_value": 0.0,
            "average_discount_pct": 0.0,
            "loss_making_items": 0,
            "loss_item_ratio_pct": 0.0,
            "loss_making_orders": 0,
            "loss_order_ratio_pct": 0.0,
            "total_customers": 0,
            "loss_total_amount": 0.0
        }

    # Core aggregations
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())

    # Safe profit margin computation (handle zero sales defensively)
    profit_margin_pct = (total_profit / total_sales * 100.0) if total_sales > 0 else 0.0

    # Total distinct orders vs total line-item records
    total_items = len(df)
    total_orders = int(df["Order ID"].nunique()) if "Order ID" in df.columns else total_items

    # Units sold
    units_sold = int(df["Quantity"].sum()) if "Quantity" in df.columns else 0

    # Average Order Value (AOV) = Total Sales / Distinct Orders (avoid double-counting items)
    average_order_value = (total_sales / total_orders) if total_orders > 0 else 0.0

    # Average Discount %
    avg_discount = float(df["Discount"].mean() * 100.0) if "Discount" in df.columns else 0.0

    # Total distinct customers
    total_customers = int(df["Customer ID"].nunique()) if "Customer ID" in df.columns else 0

    # Loss-making analysis at line-item level
    loss_items_mask = df["Profit"] < 0
    loss_making_items = int(loss_items_mask.sum())
    loss_item_ratio_pct = (loss_making_items / total_items * 100.0) if total_items > 0 else 0.0
    loss_total_amount = float(df.loc[loss_items_mask, "Profit"].sum())  # negative float

    # Loss-making analysis at order level (aggregate profit per order)
    if "Order ID" in df.columns:
        order_profit = df.groupby("Order ID")["Profit"].sum()
        loss_orders_count = int((order_profit < 0).sum())
        loss_order_ratio_pct = (loss_orders_count / total_orders * 100.0) if total_orders > 0 else 0.0
    else:
        loss_orders_count = loss_making_items
        loss_order_ratio_pct = loss_item_ratio_pct

    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "profit_margin_pct": round(profit_margin_pct, 2),
        "total_orders": total_orders,
        "total_items": total_items,
        "units_sold": units_sold,
        "average_order_value": round(average_order_value, 2),
        "average_discount_pct": round(avg_discount, 2),
        "loss_making_items": loss_making_items,
        "loss_item_ratio_pct": round(loss_item_ratio_pct, 2),
        "loss_making_orders": loss_orders_count,
        "loss_order_ratio_pct": round(loss_order_ratio_pct, 2),
        "total_customers": total_customers,
        "loss_total_amount": round(loss_total_amount, 2)
    }


def aggregate_by_dimension(
    df: pd.DataFrame,
    dimension_col: str
) -> pd.DataFrame:
    """
    Aggregate metrics by any categorical dimension (Category, Region, Segment, etc.).

    Parameters
    ----------
    df : pd.DataFrame
        Transactions dataframe.
    dimension_col : str
        Column name to group by.

    Returns
    -------
    pd.DataFrame
        Aggregated table with Sales, Profit, Profit Margin %, Distinct Orders, Units Sold.
    """
    if df.empty or dimension_col not in df.columns:
        return pd.DataFrame(columns=[
            dimension_col, "Sales", "Profit", "Profit Margin %",
            "Orders", "Units Sold", "Loss Making Items"
        ])

    grouped = df.groupby(dimension_col, as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique") if "Order ID" in df.columns else ("Sales", "count"),
        Units_Sold=("Quantity", "sum") if "Quantity" in df.columns else ("Sales", "count"),
        Loss_Items=("Profit", lambda s: int((s < 0).sum()))
    )

    grouped.rename(columns={"Units_Sold": "Units Sold", "Loss_Items": "Loss Making Items"}, inplace=True)

    # Compute Profit Margin % with safe division
    grouped["Profit Margin %"] = np.where(
        grouped["Sales"] > 0,
        (grouped["Profit"] / grouped["Sales"]) * 100.0,
        0.0
    ).round(2)

    grouped["Sales"] = grouped["Sales"].round(2)
    grouped["Profit"] = grouped["Profit"].round(2)

    return grouped.sort_values(by="Sales", ascending=False).reset_index(drop=True)


def aggregate_time_series(
    df: pd.DataFrame,
    freq: str = "ME"
) -> pd.DataFrame:
    """
    Aggregate sales and profits chronologically by month or quarter.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned transactions DataFrame.
    freq : str
        Resampling frequency ('ME' for Month End, 'QE' for Quarter End).

    Returns
    -------
    pd.DataFrame
        Time series table sorted chronologically.
    """
    if df.empty or "Order Date" not in df.columns:
        return pd.DataFrame(columns=["Period", "Sales", "Profit", "Profit Margin %", "Orders"])

    temp = df.copy()
    temp["Order Date"] = pd.to_datetime(temp["Order Date"])
    temp = temp.set_index("Order Date")

    resampled = temp.resample(freq).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique") if "Order ID" in temp.columns else ("Sales", "count"),
        Units=("Quantity", "sum") if "Quantity" in temp.columns else ("Sales", "count")
    ).reset_index()

    # Format period label
    if freq.startswith("M"):
        resampled["Period"] = resampled["Order Date"].dt.strftime("%b %Y")
        resampled["YearMonth"] = resampled["Order Date"].dt.strftime("%Y-%m")
    else:
        resampled["Period"] = resampled["Order Date"].dt.to_period("Q").astype(str)
        resampled["YearMonth"] = resampled["Period"]

    resampled["Profit Margin %"] = np.where(
        resampled["Sales"] > 0,
        (resampled["Profit"] / resampled["Sales"]) * 100.0,
        0.0
    ).round(2)

    resampled["Sales"] = resampled["Sales"].round(2)
    resampled["Profit"] = resampled["Profit"].round(2)

    return resampled


def get_product_rankings(
    df: pd.DataFrame,
    top_n: int = 10
) -> Dict[str, pd.DataFrame]:
    """
    Return top performers by sales and bottom loss-makers by profit.

    Parameters
    ----------
    df : pd.DataFrame
        Transactions dataframe.
    top_n : int
        Number of items to retrieve in each tier.

    Returns
    -------
    Dict[str, pd.DataFrame]
        DataFrames for top sales, top profit, and deepest loss-making products.
    """
    prod_col = "Product Name" if "Product Name" in df.columns else "Product ID"
    if df.empty or prod_col not in df.columns:
        empty = pd.DataFrame(columns=[prod_col, "Sales", "Profit", "Profit Margin %", "Units Sold"])
        return {"top_sales": empty, "top_profit": empty, "worst_losses": empty}

    agg = df.groupby([prod_col, "Category"], as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum") if "Quantity" in df.columns else ("Sales", "count"),
        Orders=("Order ID", "nunique") if "Order ID" in df.columns else ("Sales", "count")
    )
    agg.rename(columns={"Units_Sold": "Units Sold"}, inplace=True)
    agg["Profit Margin %"] = np.where(
        agg["Sales"] > 0,
        (agg["Profit"] / agg["Sales"]) * 100.0,
        0.0
    ).round(2)
    agg["Sales"] = agg["Sales"].round(2)
    agg["Profit"] = agg["Profit"].round(2)

    top_sales = agg.sort_values(by="Sales", ascending=False).head(top_n).reset_index(drop=True)
    top_profit = agg.sort_values(by="Profit", ascending=False).head(top_n).reset_index(drop=True)
    worst_losses = agg.sort_values(by="Profit", ascending=True).head(top_n).reset_index(drop=True)

    return {
        "top_sales": top_sales,
        "top_profit": top_profit,
        "worst_losses": worst_losses
    }
