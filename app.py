"""
Retail Sales & Profit Intelligence Platform
===========================================
Enterprise SaaS Analytics & Decision Platform
Designed for Executive Portfolios, Commercial Operations & Boardroom BI.
Built with Streamlit, Plotly, and Pandas.
"""

import io
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd
import streamlit as st

# Add src to path for module resolution
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import inspect_raw_data, load_dataset
from src.data_cleaner import clean_retail_data
from src.eda import (
    detect_outliers_iqr,
    get_category_frequency,
    get_descriptive_statistics,
    get_dataset_overview,
    get_plain_english_interpretations,
    get_sampling_subsets
)
from src.insights import generate_business_insights
from src.metrics import (
    aggregate_by_dimension,
    aggregate_time_series,
    calculate_kpis,
    get_product_rankings
)
from src.visualizations import (
    THEME,
    plot_category_performance,
    plot_discount_vs_profit,
    plot_monthly_trend,
    plot_regional_comparison,
    plot_sales_distribution,
    plot_state_choropleth,
    plot_subcategory_performance
)

# -----------------------------------------------------------------------------
# 1. Page Configuration & Enterprise Design System (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Retail Intelligence | Enterprise BI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Enterprise CSS (Light Theme, Indigo Accents, Tabular Numerals)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Hide Streamlit Top Chrome Header & Decoration */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }

    /* Global typography and background */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #F5F7FA !important;
        color: #172033 !important;
    }

    /* Main container padding tuned for 1366x768 first-viewport */
    .block-container {
        padding-top: 0.65rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1400px !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 0.75rem !important;
    }
    [data-testid="stSidebar"] hr {
        margin: 10px 0 !important;
        border-color: #E2E8F0 !important;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 2px 0 8px 0;
    }
    .brand-logo {
        background: #4F46E5;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 12px;
        width: 26px;
        height: 26px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        letter-spacing: -0.02em;
    }
    .brand-text {
        font-size: 14px;
        font-weight: 700;
        color: #172033;
        line-height: 1.1;
    }
    .brand-sub {
        font-size: 10px;
        color: #64748B;
        font-weight: 400;
    }
    .sidebar-section-title {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
        margin: 10px 0 4px 0;
    }

    /* Compact Multiselect Tags in Sidebar */
    [data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #EEF2FF !important;
        color: #4F46E5 !important;
        border: 1px solid #E0E7FF !important;
        font-size: 10px !important;
        padding: 0 4px !important;
        height: 18px !important;
        margin: 1px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        min-height: 30px !important;
        font-size: 12px !important;
    }

    /* Sleek Top Utility Header (44px height) */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 8px 14px;
        margin-bottom: 10px;
    }
    .top-header-left {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .top-header-title {
        font-size: 16px;
        font-weight: 700;
        color: #172033;
        margin: 0;
        line-height: 1.1;
    }
    .top-header-sep {
        color: #CBD5E1;
        font-size: 14px;
    }
    .top-header-subtitle {
        font-size: 11px;
        color: #64748B;
    }
    .badge-container {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .status-badge {
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        white-space: nowrap;
    }
    .status-badge-indigo {
        background: #EEF2FF;
        color: #4F46E5;
        border-color: #E0E7FF;
    }

    /* KPI Cards Grid (Compact 74px height) */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        margin-bottom: 12px;
    }
    @media (max-width: 1024px) {
        .kpi-grid {
            grid-template-columns: repeat(3, 1fr);
        }
    }
    @media (max-width: 768px) {
        .kpi-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    .kpi-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 10px 14px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 72px;
    }
    .kpi-title {
        font-size: 10px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 2px;
    }
    .kpi-value {
        font-size: 21px;
        font-weight: 700;
        color: #172033;
        font-variant-numeric: tabular-nums;
        line-height: 1.15;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-meta {
        font-size: 10.5px;
        color: #64748B;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
        white-space: nowrap;
    }
    .text-positive { color: #0F9D78 !important; font-weight: 600; }
    .text-negative { color: #DC4C4C !important; font-weight: 600; }
    .text-neutral  { color: #64748B !important; }

    /* Native Container Border Card Styling */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
    }

    .card-heading {
        font-size: 13px;
        font-weight: 600;
        color: #172033;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 0px;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 6px 14px;
        font-size: 12.5px;
        font-weight: 500;
        color: #64748B;
        background: transparent;
        border-radius: 4px 4px 0 0;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: #4F46E5 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #4F46E5 !important;
        background: transparent !important;
    }

    /* Insights Callout Boxes */
    .insight-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #4F46E5;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .insight-card.danger { border-left-color: #DC4C4C; }
    .insight-card.warning { border-left-color: #F59E0B; }
    .insight-card.success { border-left-color: #0F9D78; }
    .insight-card.info { border-left-color: #4F46E5; }

    .insight-tag {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 2px;
    }
    .insight-headline {
        font-size: 13.5px;
        font-weight: 600;
        color: #172033;
        margin-bottom: 4px;
    }
    .insight-text {
        font-size: 12px;
        color: #475569;
        line-height: 1.45;
        margin-bottom: 6px;
    }
    .insight-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        background: #F8FAFC;
        border: 1px solid #F1F5F9;
        border-radius: 4px;
        padding: 5px 8px;
        font-size: 11px;
        color: #475569;
        margin-bottom: 6px;
    }
    .insight-rec {
        font-size: 11.5px;
        color: #172033;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Data Ingestion & Caching Layer
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_or_load_dataset(source_option: str, uploaded_bytes: Optional[bytes] = None, file_name: Optional[str] = None):
    """Load, inspect, and clean the retail transaction dataset with caching."""
    if uploaded_bytes is not None and file_name is not None:
        buffer = io.BytesIO(uploaded_bytes)
        raw_df, meta = load_dataset(buffer, file_name=file_name)
    elif source_option == "Cleaned Dataset (Default)":
        cleaned_path = Path("data/processed/cleaned_superstore.csv")
        if cleaned_path.exists():
            cleaned_df = pd.read_csv(cleaned_path)
            cleaned_df["Order Date"] = pd.to_datetime(cleaned_df["Order Date"])
            cleaned_df["Ship Date"] = pd.to_datetime(cleaned_df["Ship Date"])
            report = {
                "raw_row_count": len(cleaned_df),
                "cleaned_row_count": len(cleaned_df),
                "rows_retained_pct": 100.0,
                "data_quality_issues": ["Pre-cleaned standard dataset loaded."],
                "date_range": (
                    cleaned_df["Order Date"].min().strftime("%Y-%m-%d"),
                    cleaned_df["Order Date"].max().strftime("%Y-%m-%d")
                )
            }
            return cleaned_df, cleaned_df, report, {"file_name": "cleaned_superstore.csv", "format": "CSV"}
        else:
            raw_path = Path("data/raw/sample_superstore_raw.csv")
            raw_df, meta = load_dataset(raw_path)
    else:
        raw_path = Path("data/raw/sample_superstore_raw.csv")
        raw_df, meta = load_dataset(raw_path)

    cleaned_df, report_obj = clean_retail_data(
        raw_df,
        export_cleaned_path="data/processed/cleaned_superstore.csv"
    )
    return raw_df, cleaned_df, report_obj.to_dict(), meta


# -----------------------------------------------------------------------------
# 3. Sidebar: Compact Enterprise Layout
# -----------------------------------------------------------------------------
with st.sidebar:
    # Brand mark
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-logo">RI</div>
        <div>
            <div class="brand-text">Retail Intelligence</div>
            <div class="brand-sub">Sales & Profit Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Data Source Section
    st.markdown('<div class="sidebar-section-title">Data Source</div>', unsafe_allow_html=True)
    source_choice = st.selectbox(
        "Source",
        options=["Cleaned Dataset (Default)", "Raw Superstore (Live Cleansing)", "Upload Custom File (CSV/Excel)"],
        index=0,
        label_visibility="collapsed"
    )

    uploaded_file = None
    if source_choice == "Upload Custom File (CSV/Excel)":
        uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx", "xls"], label_visibility="collapsed")

    # Load Data
    try:
        if uploaded_file is not None:
            raw_df, cleaned_df, report_dict, meta_info = get_or_load_dataset(
                source_choice,
                uploaded_bytes=uploaded_file.getvalue(),
                file_name=uploaded_file.name
            )
        else:
            raw_df, cleaned_df, report_dict, meta_info = get_or_load_dataset(source_choice)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()

    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Filters</div>', unsafe_allow_html=True)

    # 1. Date Range Filter
    min_date = cleaned_df["Order Date"].min().date()
    max_date = cleaned_df["Order Date"].max().date()

    date_range = st.date_input(
        "Order Date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="filter_dates"
    )

    # 2. Region Filter
    all_regions = sorted(cleaned_df["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
        key="filter_regions"
    )

    # 3. Category Filter
    all_categories = sorted(cleaned_df["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Category",
        options=all_categories,
        default=all_categories,
        key="filter_categories"
    )

    # 4. Sub-Category Filter (dynamic based on category selection)
    available_subcats = sorted(
        cleaned_df[cleaned_df["Category"].isin(selected_categories)]["Sub-Category"].dropna().unique().tolist()
    )
    selected_subcats = st.multiselect(
        "Sub-Category",
        options=available_subcats,
        default=available_subcats,
        key="filter_subcategories"
    )

    # 5. Segment Filter
    all_segments = sorted(cleaned_df["Segment"].dropna().unique().tolist())
    selected_segments = st.multiselect(
        "Customer Segment",
        options=all_segments,
        default=all_segments,
        key="filter_segments"
    )

    # Reset button
    if st.button("Reset Filters", use_container_width=True):
        for k in ["filter_regions", "filter_categories", "filter_subcategories", "filter_segments", "filter_dates"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Data Actions</div>', unsafe_allow_html=True)

    # Exports
    cleaned_csv = cleaned_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Cleaned Dataset (CSV)",
        data=cleaned_csv,
        file_name="cleaned_superstore.csv",
        mime="text/csv",
        use_container_width=True
    )


# -----------------------------------------------------------------------------
# 4. Filter Processing & Defensive Handling
# -----------------------------------------------------------------------------
filtered_df = cleaned_df.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_d) &
        (filtered_df["Order Date"].dt.date <= end_d)
    ]

if selected_regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]
if selected_categories:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
if selected_subcats:
    filtered_df = filtered_df[filtered_df["Sub-Category"].isin(selected_subcats)]
if selected_segments:
    filtered_df = filtered_df[filtered_df["Segment"].isin(selected_segments)]

# Download Filtered Data in Sidebar
with st.sidebar:
    filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Filtered View (CSV)",
        data=filtered_csv,
        file_name="filtered_view.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown(f"""
    <div style="font-size: 10.5px; color: #94A3B8; margin-top: 12px; line-height: 1.4;">
        Active records: <b>{len(filtered_df):,}</b> / {len(cleaned_df):,}<br>
        Source: {meta_info.get('file_name', 'Superstore')}
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 5. Compact Header & Metric Calculation
# -----------------------------------------------------------------------------
active_start = filtered_df["Order Date"].min().strftime("%b %d, %Y") if not filtered_df.empty else "N/A"
active_end = filtered_df["Order Date"].max().strftime("%b %d, %Y") if not filtered_df.empty else "N/A"

st.markdown(f"""
<div class="top-header">
    <div class="top-header-left">
        <h1 class="top-header-title">Sales & Profit Overview</h1>
        <span class="top-header-sep">/</span>
        <span class="top-header-subtitle">Omnichannel Commercial Operations & Margin Health</span>
    </div>
    <div class="badge-container">
        <span class="status-badge status-badge-indigo">📅 {active_start} — {active_end}</span>
        <span class="status-badge">📦 {len(filtered_df):,} active line items</span>
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No transactions match the selected filters. Please adjust the sidebar filters.")
    st.stop()

# Compute KPIs
kpis = calculate_kpis(filtered_df)

# Compact 5-card KPI Grid
profit_color = "text-positive" if kpis["total_profit"] >= 0 else "text-negative"
margin_color = "text-positive" if kpis["profit_margin_pct"] >= 10 else ("text-negative" if kpis["profit_margin_pct"] < 0 else "text-neutral")

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-box">
        <div class="kpi-title">Total Sales</div>
        <div class="kpi-value">${kpis['total_sales']:,.0f}</div>
        <div class="kpi-meta">Avg ticket: <b>${kpis['average_order_value']:,.0f}</b></div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">Net Profit</div>
        <div class="kpi-value {profit_color}">${kpis['total_profit']:,.0f}</div>
        <div class="kpi-meta">Loss items: <b class="text-negative">{kpis['loss_making_items']:,}</b></div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">Profit Margin</div>
        <div class="kpi-value {margin_color}">{kpis['profit_margin_pct']:.1f}%</div>
        <div class="kpi-meta">Net margin on sales</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">Total Orders</div>
        <div class="kpi-value">{kpis['total_orders']:,}</div>
        <div class="kpi-meta">Distinct order IDs</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">Units Sold</div>
        <div class="kpi-value">{kpis['units_sold']:,}</div>
        <div class="kpi-meta">Avg discount: <b>{kpis['average_discount_pct']:.1f}%</b></div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. Tabbed Multi-Page Navigation (Clean, Professional Labels)
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "Executive Overview",
    "Sales Analysis",
    "Profitability",
    "Geography",
    "Data Quality & EDA",
    "Business Insights"
])


# =============================================================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================================================
with tabs[0]:
    # Row 2: Monthly Trend (67% width) + Category Contribution (33% width)
    col_row2_1, col_row2_2 = st.columns([67, 33])

    with col_row2_1:
        with st.container(border=True):
            ts_df = aggregate_time_series(filtered_df, freq="ME")
            if not ts_df.empty:
                st.plotly_chart(plot_monthly_trend(ts_df), use_container_width=True)
            else:
                st.info("Insufficient time-series data for monthly trend.")

    with col_row2_2:
        with st.container(border=True):
            cat_df = aggregate_by_dimension(filtered_df, "Category")
            st.plotly_chart(plot_category_performance(cat_df), use_container_width=True)

    # Row 3: Regional Performance (50%) + Executive Summary Callout (50%)
    col_row3_1, col_row3_2 = st.columns([50, 50])

    with col_row3_1:
        with st.container(border=True):
            reg_df = aggregate_by_dimension(filtered_df, "Region")
            st.plotly_chart(plot_regional_comparison(reg_df), use_container_width=True)

    with col_row3_2:
        with st.container(border=True):
            st.markdown('<div class="card-heading">Executive Performance Summary</div>', unsafe_allow_html=True)

            top_cat = cat_df.iloc[0]["Category"] if not cat_df.empty else "N/A"
            top_cat_sales = cat_df.iloc[0]["Sales"] if not cat_df.empty else 0
            top_reg = reg_df.sort_values(by="Profit Margin %", ascending=False).iloc[0]["Region"] if not reg_df.empty else "N/A"
            top_reg_margin = reg_df.sort_values(by="Profit Margin %", ascending=False).iloc[0]["Profit Margin %"] if not reg_df.empty else 0

            st.markdown(f"""
            <div style="font-size: 12.5px; color: #475569; line-height: 1.55;">
                <p style="margin-bottom: 6px;">
                    <b>Revenue Generation:</b> Total gross sales reached <b>${kpis['total_sales']:,.2f}</b> across 
                    <b>{kpis['total_orders']:,}</b> orders, maintaining an Average Order Value (AOV) of <b>${kpis['average_order_value']:,.2f}</b>.
                </p>
                <p style="margin-bottom: 6px;">
                    <b>Category Anchor:</b> <b>{top_cat}</b> is the leading sales volume driver (<b>${top_cat_sales:,.2f}</b>).
                </p>
                <p style="margin-bottom: 6px;">
                    <b>Regional Margin Leader:</b> <b>{top_reg}</b> generated the highest operating efficiency at 
                    <b>{top_reg_margin:.1f}% profit margin</b>.
                </p>
                <p style="margin-bottom: 0;">
                    <b>Margin Exposure:</b> <b>{kpis['loss_making_items']:,} transactions ({kpis['loss_item_ratio_pct']:.1f}%)</b> 
                    were fulfilled at negative net profit, accumulating <span class="text-negative">-${abs(kpis['loss_total_amount']):,.2f}</span> in preventable margin leakage.
                </p>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: SALES ANALYSIS
# =============================================================================
with tabs[1]:
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        with st.container(border=True):
            subcat_df = aggregate_by_dimension(filtered_df, "Sub-Category")
            st.plotly_chart(
                plot_category_performance(subcat_df.head(8).rename(columns={"Sub-Category": "Category"})),
                use_container_width=True
            )

    with col_s2:
        with st.container(border=True):
            seg_df = aggregate_by_dimension(filtered_df, "Segment")
            st.plotly_chart(
                plot_category_performance(seg_df.rename(columns={"Segment": "Category"})),
                use_container_width=True
            )

    col_s3, col_s4 = st.columns([55, 45])

    with col_s3:
        with st.container(border=True):
            st.plotly_chart(plot_sales_distribution(filtered_df), use_container_width=True)

    with col_s4:
        with st.container(border=True):
            st.markdown('<div class="card-heading">Top 10 Products by Sales Volume</div>', unsafe_allow_html=True)
            rankings = get_product_rankings(filtered_df, top_n=10)
            st.dataframe(
                rankings["top_sales"][["Product Name", "Category", "Sales", "Profit", "Profit Margin %"]],
                column_config={
                    "Sales": st.column_config.NumberColumn(format="$%.0f"),
                    "Profit": st.column_config.NumberColumn(format="$%.0f"),
                    "Profit Margin %": st.column_config.NumberColumn(format="%.1f%%")
                },
                hide_index=True,
                use_container_width=True
            )


# =============================================================================
# TAB 3: PROFITABILITY ANALYSIS
# =============================================================================
with tabs[2]:
    col_p1, col_p2 = st.columns([58, 42])

    with col_p1:
        with st.container(border=True):
            st.plotly_chart(plot_discount_vs_profit(filtered_df), use_container_width=True)
            st.markdown("""
            <div style="font-size: 11px; color: #64748B; margin-top: 4px;">
                <b>Analytical Finding:</b> Promotional discount rates exceeding 20% consistently breach gross profit thresholds, 
                producing negative margins across high-volume items.
            </div>
            """, unsafe_allow_html=True)

    with col_p2:
        with st.container(border=True):
            subcat_agg = aggregate_by_dimension(filtered_df, "Sub-Category")
            st.plotly_chart(plot_subcategory_performance(subcat_agg), use_container_width=True)

    with st.container(border=True):
        st.markdown('<div class="card-heading">Deepest Loss-Making Products (Remediation Required)</div>', unsafe_allow_html=True)
        worst_losses = rankings["worst_losses"]
        st.dataframe(
            worst_losses[["Product Name", "Category", "Sales", "Profit", "Profit Margin %", "Units Sold"]],
            column_config={
                "Sales": st.column_config.NumberColumn(format="$%.0f"),
                "Profit": st.column_config.NumberColumn(format="$%.0f"),
                "Profit Margin %": st.column_config.NumberColumn(format="%.1f%%"),
                "Units Sold": st.column_config.NumberColumn(format="%d")
            },
            hide_index=True,
            use_container_width=True
        )


# =============================================================================
# TAB 4: GEOGRAPHIC ANALYSIS
# =============================================================================
with tabs[3]:
    with st.container(border=True):
        st.plotly_chart(plot_state_choropleth(filtered_df), use_container_width=True)

    col_g1, col_g2 = st.columns(2)
    state_agg = aggregate_by_dimension(filtered_df, "State")

    with col_g1:
        with st.container(border=True):
            st.markdown('<div class="card-heading">Top 10 Profitable States</div>', unsafe_allow_html=True)
            top_states = state_agg.sort_values(by="Profit", ascending=False).head(10)
            st.dataframe(
                top_states[["State", "Sales", "Profit", "Profit Margin %", "Orders"]],
                column_config={
                    "Sales": st.column_config.NumberColumn(format="$%.0f"),
                    "Profit": st.column_config.NumberColumn(format="$%.0f"),
                    "Profit Margin %": st.column_config.NumberColumn(format="%.1f%%"),
                    "Orders": st.column_config.NumberColumn(format="%d")
                },
                hide_index=True,
                use_container_width=True
            )

    with col_g2:
        with st.container(border=True):
            st.markdown('<div class="card-heading">Bottom 10 States by Profitability</div>', unsafe_allow_html=True)
            bottom_states = state_agg.sort_values(by="Profit", ascending=True).head(10)
            st.dataframe(
                bottom_states[["State", "Sales", "Profit", "Profit Margin %", "Orders"]],
                column_config={
                    "Sales": st.column_config.NumberColumn(format="$%.0f"),
                    "Profit": st.column_config.NumberColumn(format="$%.0f"),
                    "Profit Margin %": st.column_config.NumberColumn(format="%.1f%%"),
                    "Orders": st.column_config.NumberColumn(format="%d")
                },
                hide_index=True,
                use_container_width=True
            )


# =============================================================================
# TAB 5: DATA QUALITY & EDA
# =============================================================================
with tabs[4]:
    # Audit Metrics
    with st.container(border=True):
        st.markdown('<div class="card-heading">Data Ingestion & Quality Audit</div>', unsafe_allow_html=True)
        
        dq1, dq2, dq3, dq4 = st.columns(4)
        dq1.metric("Raw Rows", f"{report_dict.get('raw_row_count', 0):,}")
        dq2.metric("Cleaned Rows", f"{report_dict.get('cleaned_row_count', 0):,}")
        dq3.metric("Retention %", f"{report_dict.get('rows_retained_pct', 100):.1f}%")
        dq4.metric("Deduplicated", f"{report_dict.get('duplicate_rows_dropped', 0):,}")

        if report_dict.get("data_quality_issues"):
            st.markdown("<div style='margin-top: 8px; font-size: 11.5px; color: #475569;'><b>Transformation Audit Log:</b></div>", unsafe_allow_html=True)
            for issue in report_dict["data_quality_issues"]:
                st.markdown(f"<div style='font-size: 11px; color: #64748B;'>• {issue}</div>", unsafe_allow_html=True)

    # Descriptive Stats
    with st.container(border=True):
        st.markdown('<div class="card-heading">Descriptive Statistics & Quartiles</div>', unsafe_allow_html=True)
        stats_df = get_descriptive_statistics(filtered_df)
        st.dataframe(stats_df, hide_index=True, use_container_width=True)

    # Outlier Detection
    with st.container(border=True):
        st.markdown('<div class="card-heading">Tukey\'s IQR Outlier Analysis</div>', unsafe_allow_html=True)
        outliers_data = detect_outliers_iqr(filtered_df)
        outlier_rows = []
        for col_name, info in outliers_data.items():
            outlier_rows.append({
                "Column": col_name,
                "Q1 (25%)": info["q1"],
                "Q3 (75%)": info["q3"],
                "IQR": info["iqr"],
                "Lower Fence": info["lower_fence"],
                "Upper Fence": info["upper_fence"],
                "Outliers": info["outlier_count"],
                "Outlier %": f"{info['outlier_percentage']:.2f}%"
            })
        st.dataframe(pd.DataFrame(outlier_rows), hide_index=True, use_container_width=True)

    # Plain English Statistical Explanations
    with st.container(border=True):
        st.markdown('<div class="card-heading">Plain-English Statistical Takeaways</div>', unsafe_allow_html=True)
        interpretations = get_plain_english_interpretations(stats_df, outliers_data, kpis)
        for interp in interpretations:
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 8px 12px; margin-bottom: 6px;">
                <div style="font-size: 11.5px; font-weight: 600; color: #172033; margin-bottom: 2px;">{interp['Topic']}</div>
                <div style="font-size: 11.5px; color: #475569;">{interp['Takeaway']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Sampling Demonstrator
    with st.container(border=True):
        st.markdown('<div class="card-heading">Scientific Sampling Subsets (Seed = 42)</div>', unsafe_allow_html=True)
        samples = get_sampling_subsets(filtered_df, sample_size=8, random_seed=42)
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.markdown("<div style='font-size: 11.5px; font-weight: 600; color: #475569; margin-bottom: 4px;'>Simple Random Sample (n=8)</div>", unsafe_allow_html=True)
            st.dataframe(samples["random_sample"][["Order ID", "Category", "Sub-Category", "Sales", "Profit"]], hide_index=True, use_container_width=True)
        with s_col2:
            st.markdown("<div style='font-size: 11.5px; font-weight: 600; color: #475569; margin-bottom: 4px;'>Stratified Sample (n=8)</div>", unsafe_allow_html=True)
            st.dataframe(samples["stratified_sample"][["Order ID", "Category", "Sub-Category", "Sales", "Profit"]], hide_index=True, use_container_width=True)


# =============================================================================
# TAB 6: BUSINESS INSIGHTS & RECOMMENDATIONS
# =============================================================================
with tabs[5]:
    st.markdown('<div style="font-size: 12px; color: #64748B; margin-bottom: 10px;">Data-driven executive recommendations dynamically calculated from the active dataset.</div>', unsafe_allow_html=True)

    insights = generate_business_insights(filtered_df, kpis)

    for item in insights:
        box_type = item.get("type", "info")
        st.markdown(f"""
        <div class="insight-card {box_type}">
            <div class="insight-tag">{item['area']}</div>
            <div class="insight-headline">{item['title']}</div>
            <div class="insight-text">{item['finding']}</div>
            <div class="insight-pills">
                <span><b>Supporting Metric:</b> {item['supporting_metric']}</span>
                <span><b>Benchmark:</b> {item['comparison']}</span>
            </div>
            <div class="insight-rec">
                🎯 <b>Management Action:</b> {item['recommendation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
