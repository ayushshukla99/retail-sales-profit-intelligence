"""
Visualizations Module for Retail Sales & Profit Intelligence Platform
======================================================================
Produces professional, interactive Plotly visualizations and static
publication-quality Matplotlib/Seaborn figures matching enterprise SaaS analytics:
- App canvas: #F5F7FA
- Main surfaces: #FFFFFF
- Deep navy typography: #172033
- Secondary labels: #64748B
- Primary accent: #4F46E5 (Indigo)
- Positive performance: #0F9D78 (Emerald)
- Negative performance: #DC4C4C (Crimson)
- Subtle accent background: #EEF2FF
- Gridlines: #E9EDF3, Borders: #E2E8F0
"""

from pathlib import Path
from typing import Dict, List, Optional, Union
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns


# Enterprise SaaS Color Palette
THEME = {
    "app_bg": "#F5F7FA",
    "surface": "#FFFFFF",
    "primary": "#4F46E5",        # Indigo
    "primary_subtle": "#EEF2FF", # Light Indigo
    "positive": "#0F9D78",       # Emerald Green
    "negative": "#DC4C4C",       # Crimson Red
    "text_primary": "#172033",   # Deep Navy
    "text_secondary": "#64748B", # Slate
    "border": "#E2E8F0",
    "grid": "#E9EDF3",
    "neutral_bar": "#CBD5E1",
    "amber": "#F59E0B"
}

FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"


def apply_base_layout(fig: go.Figure, title: str, x_title: str = "", y_title: str = "") -> go.Figure:
    """Apply consistent, restrained enterprise styling to Plotly figures."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "y": 0.96,
            "x": 0.02,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"size": 14, "color": THEME["text_primary"], "family": FONT_FAMILY}
        },
        font={"family": FONT_FAMILY, "color": THEME["text_secondary"], "size": 11},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=36, r=24, t=44, b=32),
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=11, color=THEME["text_secondary"])),
            showgrid=True,
            gridcolor=THEME["grid"],
            gridwidth=1,
            linecolor=THEME["border"],
            tickfont=dict(size=10, color=THEME["text_secondary"]),
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=11, color=THEME["text_secondary"])),
            showgrid=True,
            gridcolor=THEME["grid"],
            gridwidth=1,
            linecolor=THEME["border"],
            tickfont=dict(size=10, color=THEME["text_secondary"]),
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=THEME["text_secondary"])
        ),
        hoverlabel=dict(
            bgcolor=THEME["text_primary"],
            font_size=11,
            font_family=FONT_FAMILY,
            font_color="#FFFFFF"
        )
    )
    return fig


def plot_monthly_trend(ts_df: pd.DataFrame) -> go.Figure:
    """Dual-axis line chart for Monthly Sales and Profit trend."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Sales line (Indigo)
    fig.add_trace(
        go.Scatter(
            x=ts_df["Period"],
            y=ts_df["Sales"],
            name="Sales",
            mode="lines+markers",
            line=dict(color=THEME["primary"], width=2),
            marker=dict(size=4, color=THEME["primary"]),
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>"
        ),
        secondary_y=False
    )

    # Profit line (Emerald)
    fig.add_trace(
        go.Scatter(
            x=ts_df["Period"],
            y=ts_df["Profit"],
            name="Profit",
            mode="lines+markers",
            line=dict(color=THEME["positive"], width=2),
            marker=dict(size=4, color=THEME["positive"]),
            hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_layout(
        title={
            "text": "<b>Monthly Revenue & Profit Trajectory</b>",
            "y": 0.96,
            "x": 0.02,
            "font": {"size": 14, "color": THEME["text_primary"], "family": FONT_FAMILY}
        },
        font={"family": FONT_FAMILY, "color": THEME["text_secondary"], "size": 11},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=36, r=36, t=44, b=32),
        legend=dict(orientation="h", y=1.04, x=1, xanchor="right", font=dict(size=11)),
        hovermode="x unified"
    )

    fig.update_xaxes(showgrid=True, gridcolor=THEME["grid"], tickangle=-45, tickfont=dict(size=9))
    fig.update_yaxes(title_text="Sales ($)", secondary_y=False, showgrid=True, gridcolor=THEME["grid"], tickfont=dict(size=10))
    fig.update_yaxes(title_text="Profit ($)", secondary_y=True, showgrid=False, tickfont=dict(size=10))

    return fig


def plot_category_performance(cat_df: pd.DataFrame) -> go.Figure:
    """Clustered bar chart for Category Sales and Profit."""
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=cat_df["Category"],
            y=cat_df["Sales"],
            name="Sales",
            marker_color=THEME["primary"],
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            x=cat_df["Category"],
            y=cat_df["Profit"],
            name="Profit",
            marker_color=THEME["positive"],
            hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>"
        )
    )

    apply_base_layout(fig, "Category Performance", "", "Amount ($)")
    fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.08)
    return fig


def plot_subcategory_performance(subcat_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart for Sub-Category profits highlighting loss-makers in Crimson."""
    df_sorted = subcat_df.sort_values(by="Profit", ascending=True)

    colors = [THEME["negative"] if p < 0 else THEME["positive"] for p in df_sorted["Profit"]]

    fig = go.Figure(
        go.Bar(
            x=df_sorted["Profit"],
            y=df_sorted["Sub-Category"],
            orientation="h",
            marker_color=colors,
            hovertemplate="<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>"
        )
    )

    apply_base_layout(fig, "Profit Contribution by Sub-Category", "Net Profit ($)", "")
    fig.add_vline(x=0, line_width=1, line_dash="solid", line_color=THEME["border"])
    return fig


def plot_regional_comparison(reg_df: pd.DataFrame) -> go.Figure:
    """Grouped comparison of Sales and Profit Margin % by Region."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=reg_df["Region"],
            y=reg_df["Sales"],
            name="Sales",
            marker_color=THEME["primary"],
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>"
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=reg_df["Region"],
            y=reg_df["Profit Margin %"],
            name="Margin %",
            mode="lines+markers",
            line=dict(color=THEME["amber"], width=2.5),
            marker=dict(size=6, color=THEME["amber"]),
            hovertemplate="<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_layout(
        title={
            "text": "<b>Regional Revenue & Margin Efficiency</b>",
            "y": 0.96,
            "x": 0.02,
            "font": {"size": 14, "color": THEME["text_primary"], "family": FONT_FAMILY}
        },
        font={"family": FONT_FAMILY, "color": THEME["text_secondary"], "size": 11},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=36, r=36, t=44, b=32),
        legend=dict(orientation="h", y=1.04, x=1, xanchor="right")
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="Sales ($)", secondary_y=False, showgrid=True, gridcolor=THEME["grid"])
    fig.update_yaxes(title_text="Margin %", secondary_y=True, showgrid=False)

    return fig


def plot_discount_vs_profit(df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot showing the direct empirical relationship between Discount and Profit.
    Reveals the severe margin degradation caused by aggressive discount levels.
    """
    plot_df = df.sample(n=min(2000, len(df)), random_state=42) if len(df) > 2000 else df

    fig = px.scatter(
        plot_df,
        x="Discount",
        y="Profit",
        color="Category",
        color_discrete_map={
            "Technology": THEME["primary"],
            "Office Supplies": THEME["positive"],
            "Furniture": THEME["amber"]
        },
        hover_data=["Sub-Category", "Sales", "Quantity"],
        opacity=0.65
    )

    apply_base_layout(fig, "Discount Rate vs. Realized Profit", "Discount Rate (0.0 to 0.8)", "Profit ($)")
    fig.add_hline(y=0, line_width=1.2, line_dash="solid", line_color=THEME["negative"])
    fig.add_vline(x=0.20, line_width=1, line_dash="dot", line_color=THEME["text_secondary"])

    return fig


def plot_sales_distribution(df: pd.DataFrame) -> go.Figure:
    """Distribution histogram of order Sales on logarithmic/capped scale."""
    fig = px.histogram(
        df,
        x="Sales",
        nbins=50,
        color_discrete_sequence=[THEME["primary"]],
        marginal="box",
        opacity=0.85
    )
    apply_base_layout(fig, "Transaction Ticket Size Distribution & Outliers", "Sales ($)", "Count")
    return fig


def plot_state_choropleth(df: pd.DataFrame) -> go.Figure:
    """Choropleth map of US States by Total Sales or Profit."""
    us_state_to_code = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
        'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
        'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
        'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
        'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }

    if "State" not in df.columns:
        return go.Figure()

    state_agg = df.groupby("State", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique") if "Order ID" in df.columns else ("Sales", "count")
    )
    state_agg["Code"] = state_agg["State"].map(us_state_to_code)
    state_agg = state_agg.dropna(subset=["Code"])

    state_agg["Profit Margin %"] = np.where(
        state_agg["Sales"] > 0,
        (state_agg["Profit"] / state_agg["Sales"]) * 100.0,
        0.0
    ).round(2)

    fig = go.Figure(
        data=go.Choropleth(
            locations=state_agg["Code"],
            z=state_agg["Profit"],
            locationmode="USA-states",
            colorscale=[
                [0.0, THEME["negative"]],
                [0.45, "#FEE2E2"],
                [0.5, "#F8FAFC"],
                [0.55, "#D1FAE5"],
                [1.0, THEME["positive"]]
            ],
            text=state_agg["State"] + "<br>Sales: $" + state_agg["Sales"].map("{:,.0f}".format) +
                 "<br>Margin: " + state_agg["Profit Margin %"].map("{:.1f}%".format),
            hoverinfo="location+z+text",
            colorbar=dict(
                title=dict(text="Profit ($)", font=dict(size=10, color=THEME["text_secondary"])),
                tickfont=dict(size=9, color=THEME["text_secondary"]),
                len=0.75,
                thickness=12
            )
        )
    )

    fig.update_layout(
        title={
            "text": "<b>State-Level Net Operating Profitability</b>",
            "y": 0.96,
            "x": 0.02,
            "font": {"size": 14, "color": THEME["text_primary"], "family": FONT_FAMILY}
        },
        geo=dict(
            scope="usa",
            lakecolor="#F5F7FA",
            landcolor="#FFFFFF",
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=0, r=0, t=44, b=0),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


def export_static_charts(df: pd.DataFrame, output_dir: Union[str, Path]) -> List[str]:
    """Generate high-resolution Matplotlib/Seaborn charts."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    generated_files = []

    sns.set_theme(style="whitegrid", font_scale=0.9)
    plt.rcParams["font.family"] = "sans-serif"

    # Chart 1: Monthly Trend
    if "Order YearMonth" in df.columns:
        monthly = df.groupby("Order YearMonth").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
        fig, ax1 = plt.subplots(figsize=(11, 4.5), dpi=300)
        ax2 = ax1.twinx()

        x = range(len(monthly))
        ax1.plot(x, monthly["Sales"], color=THEME["primary"], linewidth=2, marker="o", markersize=4, label="Sales ($)")
        ax2.plot(x, monthly["Profit"], color=THEME["positive"], linewidth=2, marker="s", markersize=4, label="Profit ($)")

        ax1.set_title("Monthly Sales & Profit Performance Trend", fontsize=13, weight="bold", color=THEME["text_primary"], pad=12)
        ax1.set_xlabel("Month", fontsize=10, color=THEME["text_secondary"])
        ax1.set_ylabel("Sales ($)", fontsize=10, color=THEME["primary"])
        ax2.set_ylabel("Profit ($)", fontsize=10, color=THEME["positive"])

        step = max(1, len(monthly) // 10)
        ax1.set_xticks(x[::step])
        ax1.set_xticklabels(monthly["Order YearMonth"].iloc[::step], rotation=45, ha="right", fontsize=9)

        fig.tight_layout()
        f1 = out_path / "monthly_trend.png"
        fig.savefig(f1)
        plt.close(fig)
        generated_files.append(str(f1))

    # Chart 2: Sub-Category Profit
    if "Sub-Category" in df.columns:
        subcat = df.groupby("Sub-Category")["Profit"].sum().sort_values()
        colors = [THEME["negative"] if p < 0 else THEME["positive"] for p in subcat.values]

        fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
        ax.barh(subcat.index, subcat.values, color=colors, height=0.6)
        ax.axvline(0, color=THEME["border"], linestyle="-", linewidth=1)
        ax.set_title("Net Profit by Sub-Category", fontsize=13, weight="bold", color=THEME["text_primary"], pad=12)
        ax.set_xlabel("Net Profit ($)", fontsize=10, color=THEME["text_secondary"])

        fig.tight_layout()
        f2 = out_path / "subcategory_profit.png"
        fig.savefig(f2)
        plt.close(fig)
        generated_files.append(str(f2))

    # Chart 3: Discount vs Profit Scatter
    if "Discount" in df.columns and "Profit" in df.columns:
        fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
        scatter_sample = df.sample(n=min(2500, len(df)), random_state=42)
        sns.scatterplot(
            data=scatter_sample,
            x="Discount",
            y="Profit",
            hue="Category",
            palette=[THEME["primary"], THEME["positive"], THEME["amber"]],
            alpha=0.6,
            s=25,
            ax=ax
        )
        ax.axhline(0, color=THEME["negative"], linestyle="--", linewidth=1.2, label="Break-Even ($0)")
        ax.axvline(0.20, color=THEME["text_secondary"], linestyle=":", linewidth=1, label="20% Discount Threshold")
        ax.set_title("Discount Rate vs. Profit Realization", fontsize=13, weight="bold", color=THEME["text_primary"], pad=12)
        ax.set_xlabel("Discount Rate", fontsize=10, color=THEME["text_secondary"])
        ax.set_ylabel("Profit ($)", fontsize=10, color=THEME["text_secondary"])
        ax.legend(loc="upper right", frameon=True, fontsize=9)

        fig.tight_layout()
        f3 = out_path / "discount_vs_profit.png"
        fig.savefig(f3)
        plt.close(fig)
        generated_files.append(str(f3))

    # Chart 4: Regional Performance
    if "Region" in df.columns:
        reg = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
        fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
        bar_width = 0.35
        indices = np.arange(len(reg))

        ax.bar(indices - bar_width/2, reg["Sales"], bar_width, label="Sales ($)", color=THEME["primary"])
        ax.bar(indices + bar_width/2, reg["Profit"], bar_width, label="Profit ($)", color=THEME["positive"])

        ax.set_title("Sales and Profit Across Geographic Regions", fontsize=13, weight="bold", color=THEME["text_primary"], pad=12)
        ax.set_xticks(indices)
        ax.set_xticklabels(reg["Region"], fontsize=9)
        ax.set_ylabel("Amount ($)", fontsize=10, color=THEME["text_secondary"])
        ax.legend(frameon=True, fontsize=9)

        fig.tight_layout()
        f4 = out_path / "regional_performance.png"
        fig.savefig(f4)
        plt.close(fig)
        generated_files.append(str(f4))

    return generated_files
