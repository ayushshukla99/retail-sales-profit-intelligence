"""
Report and Chart Generator Script
=================================
Automates the production of publication-ready Matplotlib/Seaborn static figures
and Markdown analysis reports for portfolio documentation and college grading.
"""

from pathlib import Path
import json
import pandas as pd
from src.data_loader import load_dataset
from src.data_cleaner import clean_retail_data
from src.metrics import calculate_kpis, aggregate_by_dimension
from src.eda import get_descriptive_statistics, detect_outliers_iqr, get_plain_english_interpretations
from src.visualizations import export_static_charts
from src.insights import generate_business_insights


def generate_all_artifacts():
    print("Ingesting raw data...")
    raw_df, meta = load_dataset("data/raw/sample_superstore_raw.csv")

    print("Executing cleaning pipeline...")
    cleaned_df, report = clean_retail_data(
        raw_df,
        export_cleaned_path="data/processed/cleaned_superstore.csv"
    )

    print("Generating static visualizations in outputs/charts/...")
    charts = export_static_charts(cleaned_df, "outputs/charts")
    print(f"Generated {len(charts)} chart figures.")

    print("Calculating metrics and generating executive summaries...")
    kpis = calculate_kpis(cleaned_df)
    stats_df = get_descriptive_statistics(cleaned_df)
    outliers = detect_outliers_iqr(cleaned_df)
    insights = generate_business_insights(cleaned_df, kpis)

    # 1. Write Data Quality Audit Report
    dq_report_path = Path("outputs/reports/data_quality_report.md")
    dq_report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dq_report_path, "w", encoding="utf-8") as f:
        f.write("# Retail Dataset Quality & Cleansing Audit Report\n\n")
        f.write(f"- **Raw Record Count:** {report.raw_row_count:,}\n")
        f.write(f"- **Cleaned Record Count:** {report.cleaned_row_count:,}\n")
        f.write(f"- **Records Retained:** {report.to_dict()['rows_retained_pct']}%\n")
        f.write(f"- **Completely Blank Rows Dropped:** {report.completely_empty_rows_dropped:,}\n")
        f.write(f"- **Duplicate Transactions Dropped:** {report.duplicate_rows_dropped:,}\n")
        f.write(f"- **Missing Key Monetary Records Handled:** {report.missing_key_records_dropped:,}\n")
        f.write(f"- **Date Range:** {report.date_range[0]} to {report.date_range[1]}\n\n")
        f.write("### Data Quality Transformation Actions\n\n")
        for issue in report.data_quality_issues:
            f.write(f"- {issue}\n")
        f.write("\n### Imputed Fields\n\n")
        for col, desc in report.imputed_columns.items():
            f.write(f"- **{col}:** {desc}\n")

    # 2. Write Executive Summary & Business Insights Report
    exec_report_path = Path("outputs/reports/executive_summary.md")
    with open(exec_report_path, "w", encoding="utf-8") as f:
        f.write("# Retail Sales & Profit Intelligence: Executive Business Report\n\n")
        f.write("## 1. Top-Level Enterprise Metrics\n\n")
        f.write(f"- **Total Gross Revenue:** ${kpis['total_sales']:,.2f}\n")
        f.write(f"- **Net Operating Profit:** ${kpis['total_profit']:,.2f}\n")
        f.write(f"- **Overall Profit Margin:** {kpis['profit_margin_pct']:.2f}%\n")
        f.write(f"- **Total Distinct Orders:** {kpis['total_orders']:,}\n")
        f.write(f"- **Total Line Items:** {kpis['total_items']:,}\n")
        f.write(f"- **Average Order Value (AOV):** ${kpis['average_order_value']:,.2f}\n")
        f.write(f"- **Loss-Making Items Rate:** {kpis['loss_item_ratio_pct']:.2f}% ({kpis['loss_making_items']:,} items)\n")
        f.write(f"- **Total Preventable Loss:** ${abs(kpis['loss_total_amount']):,.2f}\n\n")

        f.write("## 2. Key Dynamic Business Findings & Strategic Recommendations\n\n")
        for idx, item in enumerate(insights, start=1):
            f.write(f"### {idx}. {item['title']}\n")
            f.write(f"**Area:** {item['area']}\n\n")
            f.write(f"{item['finding']}\n\n")
            f.write(f"- **Metric Evidence:** {item['supporting_metric']}\n")
            f.write(f"- **Comparison:** {item['comparison']}\n")
            f.write(f"- **Actionable Recommendation:** {item['recommendation']}\n\n")

    print("Artifacts generated successfully in outputs/!")


if __name__ == "__main__":
    generate_all_artifacts()
