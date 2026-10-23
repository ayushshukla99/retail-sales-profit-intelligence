"""
Exploratory Data Analysis (EDA) Module
======================================
Provides comprehensive descriptive statistics, distribution diagnostics,
outlier detection via IQR, reproducible sampling methodologies, and plain-English
business interpretations suitable for academic submissions and executive portfolios.
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


def get_dataset_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate structural overview of columns, data types, and null counts.
    """
    overview = []
    for col in df.columns:
        s = df[col]
        dtype_str = str(s.dtype)
        null_cnt = int(s.isnull().sum())
        null_pct = round((null_cnt / max(len(df), 1)) * 100, 2)
        n_unique = int(s.nunique())
        overview.append({
            "Column": col,
            "Data Type": dtype_str,
            "Non-Null Count": len(df) - null_cnt,
            "Null Count": null_cnt,
            "Null %": null_pct,
            "Unique Values": n_unique,
            "Example Value": str(s.dropna().iloc[0]) if not s.dropna().empty else "None"
        })
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns_summary": pd.DataFrame(overview)
    }


def get_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate parametric and non-parametric summary statistics for all numeric columns.
    Includes Mean, Std Dev, Median, IQR, Min, Q1 (25%), Q3 (75%), Max, and Skewness.
    """
    numeric_cols = ["Sales", "Profit", "Quantity", "Discount"]
    available_cols = [c for c in numeric_cols if c in df.columns]

    if not available_cols:
        return pd.DataFrame()

    stats_list = []
    for col in available_cols:
        series = df[col].dropna()
        if series.empty:
            continue

        q1 = float(series.quantile(0.25))
        median = float(series.median())
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        mean = float(series.mean())
        std = float(series.std())
        skew = float(series.skew())

        stats_list.append({
            "Metric Column": col,
            "Count": int(series.count()),
            "Mean": round(mean, 2),
            "Std Dev": round(std, 2),
            "Min": round(float(series.min()), 2),
            "25% (Q1)": round(q1, 2),
            "50% (Median)": round(median, 2),
            "75% (Q3)": round(q3, 2),
            "Max": round(float(series.max()), 2),
            "IQR": round(iqr, 2),
            "Skewness": round(skew, 2)
        })

    return pd.DataFrame(stats_list)


def detect_outliers_iqr(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Detect statistical anomalies and outliers using Tukey's Interquartile Range (IQR) fence rule.
    Outlier Fences: Lower = Q1 - 1.5 * IQR, Upper = Q3 + 1.5 * IQR.
    """
    if columns is None:
        columns = [c for c in ["Sales", "Profit", "Discount"] if c in df.columns]

    results = {}
    for col in columns:
        series = df[col].dropna()
        if len(series) < 4:
            continue

        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower_fence = q1 - (1.5 * iqr)
        upper_fence = q3 + (1.5 * iqr)

        outliers_mask = (df[col] < lower_fence) | (df[col] > upper_fence)
        outlier_count = int(outliers_mask.sum())
        outlier_pct = round((outlier_count / max(len(df), 1)) * 100, 2)

        results[col] = {
            "q1": round(q1, 2),
            "q3": round(q3, 2),
            "iqr": round(iqr, 2),
            "lower_fence": round(lower_fence, 2),
            "upper_fence": round(upper_fence, 2),
            "outlier_count": outlier_count,
            "outlier_percentage": outlier_pct,
            "outlier_indices": df.index[outliers_mask].tolist()
        }

    return results


def get_sampling_subsets(
    df: pd.DataFrame,
    sample_size: int = 200,
    random_seed: int = 42
) -> Dict[str, pd.DataFrame]:
    """
    Demonstrate scientific sampling techniques:
    1. Simple Random Sampling (reproducible with fixed seed).
    2. Stratified Sampling across Category (preserving business distribution).
    """
    if df.empty:
        return {"random_sample": df, "stratified_sample": df}

    # 1. Simple Random Sample
    actual_n = min(sample_size, len(df))
    random_sample = df.sample(n=actual_n, random_state=random_seed).reset_index(drop=True)

    # 2. Stratified Sample by Category if present
    if "Category" in df.columns:
        frac = min(1.0, max(0.01, sample_size / max(len(df), 1)))
        stratified_sample = df.groupby("Category", group_keys=False).sample(
            frac=frac, random_state=random_seed
        ).reset_index(drop=True)
    else:
        stratified_sample = random_sample

    return {
        "random_sample": random_sample,
        "stratified_sample": stratified_sample
    }


def get_category_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute frequency distribution of transactions across Category and Sub-Category.
    """
    if df.empty or "Category" not in df.columns:
        return pd.DataFrame()

    freq = df.groupby(["Category", "Sub-Category"]).size().reset_index(name="Item Count")
    total = len(df)
    freq["Share %"] = (freq["Item Count"] / total * 100.0).round(2)
    return freq.sort_values(by="Item Count", ascending=False).reset_index(drop=True)


def get_plain_english_interpretations(
    stats_df: pd.DataFrame,
    outlier_dict: Dict[str, Dict[str, Any]],
    kpis: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Translate statistical metrics and distributions into clear executive takeaways.
    """
    interpretations = []

    # 1. Skewness and Distribution Insight
    sales_stats = stats_df[stats_df["Metric Column"] == "Sales"]
    if not sales_stats.empty:
        sales_mean = sales_stats["Mean"].values[0]
        sales_median = sales_stats["50% (Median)"].values[0]
        sales_skew = sales_stats["Skewness"].values[0]

        if sales_skew > 1.0:
            skew_text = (
                f"Sales distribution is heavily right-skewed (Skewness = {sales_skew:.2f}). "
                f"The mean transaction (${sales_mean:,.2f}) is substantially higher than the median (${sales_median:,.2f}). "
                "This indicates the retail model depends heavily on a small volume of high-ticket corporate enterprise purchases, "
                "while standard day-to-day purchases are much smaller."
            )
        else:
            skew_text = f"Sales distribution is symmetric with mean of ${sales_mean:,.2f}."

        interpretations.append({
            "Topic": "Sales Distribution & Skewness",
            "Takeaway": skew_text
        })

    # 2. Outliers Insight
    if "Sales" in outlier_dict and "Profit" in outlier_dict:
        sales_outliers = outlier_dict["Sales"]["outlier_count"]
        profit_outliers = outlier_dict["Profit"]["outlier_count"]
        interpretations.append({
            "Topic": "Statistical Outlier Assessment (IQR Fence)",
            "Takeaway": (
                f"Identified {sales_outliers} sales outliers ({outlier_dict['Sales']['outlier_percentage']}%) "
                f"and {profit_outliers} profit outliers ({outlier_dict['Profit']['outlier_percentage']}%). "
                "Crucially, profit outliers include extreme negative values (severe loss transactions) "
                "where deep discounting combined with high order quantity generated thousands of dollars in net losses."
            )
        })

    # 3. Overall Profitability Ratio
    margin = kpis.get("profit_margin_pct", 0)
    loss_item_pct = kpis.get("loss_item_ratio_pct", 0)
    interpretations.append({
        "Topic": "Overall Margin Health",
        "Takeaway": (
            f"The business retains an aggregate profit margin of {margin:.2f}%. "
            f"However, {loss_item_pct:.1f}% of all order line items are sold at a negative net profit. "
            "Eliminating or restructuring these loss-generating orders represents the single biggest leverage point for management."
        )
    })

    return interpretations
