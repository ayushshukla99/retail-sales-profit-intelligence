# 📊 Retail Sales & Profit Intelligence Platform
### Enterprise-Grade BI & Analytics Cockpit for Omnichannel Retail Decision Support

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Tests](https://img.shields.io/badge/Pytest-19%20Passed-brightgreen?style=flat&logo=pytest&logoColor=white)](tests/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Star%20Schema%20Ready-F2C811?style=flat&logo=powerbi&logoColor=black)](powerbi/)

---

## 1. Project Overview & Business Problem

In high-volume retail, executive leadership often focuses on top-line revenue growth while remaining blind to margin erosion happening beneath the surface. Standard accounting summaries obscure how individual discounting decisions, regional logistics overhead, and loss-leader catalog products bleed corporate capital.

The **Retail Sales & Profit Intelligence Platform** is an end-to-end, reproducible analytics system built to address this core commercial challenge:

1. **The Pricing & Discount Trap:** Identifying the precise tipping point where customer promotional discounts destroy gross profit margins.
2. **Hidden Profit Drainers:** Uncovering products and sub-categories that generate massive top-line sales while delivering deep net financial losses.
3. **Regional Inefficiency:** Diagnosing geographic disparities where fulfillment costs and market-level discounting produce substandard capital returns.
4. **Actionable Executive Guidance:** Delivering dynamic, evidence-backed recommendations for chief commercial officers, pricing committees, and supply chain managers.

---

## 2. Key Objectives & Platform Features

- **Automated Data Quality & Cleansing Engine:** Ingests CSV or Excel transaction files, handles missing fields, sanitizes anomalous dates, prevents synthetic duplicate counting, and audits all transformations.
- **Defensive Business Metric Calculations:** Computes distinct order counts, average order values (AOV), units sold, and safe zero-division margin percentages.
- **Exploratory Data Analysis & Scientific Sampling:** Computes parametric and non-parametric summary stats (Mean, Median, Std, IQR, Skewness) and demonstrates reproducible sampling (simple random and stratified sampling with fixed random seeds).
- **Interactive Streamlit Business Cockpit:** Features 6 specialized analytical views with responsive corporate styling (Deep Navy, Slate, Teal, and Rose).
- **Power BI Integration:** Fully prepared Kimball dimensional Star Schema with complete DAX measures, data model documentation, and visual guidelines.
- **Automated Artifact Generation:** Produces publication-quality Matplotlib/Seaborn static figures and Markdown audit reports in `outputs/`.

---

## 3. Technology Stack

- **Language:** Python 3.11+
- **Data Engineering:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [OpenPyXL](https://openpyxl.readthedocs.io/)
- **Interactive Web Application:** [Streamlit](https://streamlit.io/)
- **Interactive Visualizations:** [Plotly](https://plotly.com/python/)
- **Static Publication Visuals:** [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)
- **Test Automation:** [Pytest](https://docs.pytest.org/)
- **Business Intelligence Deliverable:** Microsoft Power BI (Star Schema + DAX Expressions)

---

## 4. Dataset Source & Validation

The platform analyzes the benchmark **Retail Sample Superstore Dataset** covering retail orders across the United States.
- **Source:** Tableau Public / Kaggle Official Sample Superstore benchmark repository.
- **Granularity:** Line-item transaction level.
- **Attributes:** Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit.
- **Data Quality Highlights:** The raw feed contained 10,800 rows with 806 empty trailing records, duplicate transactions, and unformatted dates. The automated cleaning pipeline normalized the data into **9,993 verified transactions** spanning **January 2015 through December 2018**.

---

## 5. Project Directory Structure

```
DV/
├── app.py                      # Main Streamlit interactive web dashboard
├── generate_reports.py         # Static charts and markdown reports generator
├── requirements.txt            # Minimal verified production dependencies
├── README.md                   # Comprehensive platform documentation
├── .gitignore                  # Git hygiene exclusions (caches, environments)
├── data/
│   ├── raw/
│   │   ├── sample_superstore_raw.csv    # Source raw CSV dataset
│   │   └── sample_superstore_raw.xlsx   # Sample Excel test dataset
│   └── processed/
│       └── cleaned_superstore.csv       # Production-cleaned dataset
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # CSV & Excel ingestion with multi-encoding fallback
│   ├── data_cleaner.py         # Non-destructive cleansing & DataQualityReport audit
│   ├── eda.py                  # Descriptive statistics, IQR fences & sampling
│   ├── metrics.py              # Executive KPIs, order deduplication & rankings
│   ├── visualizations.py       # Corporate Plotly & Matplotlib chart modules
│   └── insights.py             # Dynamic algorithmic business recommendations
├── outputs/
│   ├── charts/                 # High-resolution PNG figures for reports
│   │   ├── monthly_trend.png
│   │   ├── subcategory_profit.png
│   │   ├── discount_vs_profit.png
│   │   └── regional_performance.png
│   └── reports/                # Automated audit and executive reports
│       ├── data_quality_report.md
│       └── executive_summary.md
├── powerbi/
│   ├── dashboard_guide.md      # Full Power BI manual build & ERD guide
│   ├── dax_measures.dax        # Verified DAX formulas library
│   ├── export_star_schema.py   # Normalized Star Schema generator script
│   └── star_schema/            # Partitioned Fact & Dimension CSVs
│       ├── Fact_Sales.csv
│       ├── Dim_Product.csv
│       ├── Dim_Customer.csv
│       ├── Dim_Location.csv
│       └── Dim_Date.csv
└── tests/
    ├── test_cleaner.py         # Ingestion, missing values, duplicates tests
    ├── test_metrics.py         # KPI calculations, division by zero tests
    └── test_eda.py             # Outliers, sampling, insight generator tests
```

---

## 6. Installation & Quick Start (Windows Shell)

### Prerequisites
- Python 3.11 installed (`python --version`).
- Git (optional).

### 1. Clone or Open Workspace
```powershell
cd c:\Users\Shukla\OneDrive\Desktop\PROJECTS\DV
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run Automated Test Suite
Verify that all 19 unit tests pass:
```powershell
python -m pytest -v
```

### 4. Generate Reports & Static Visuals
Generate static charts in `outputs/charts/` and markdown summaries in `outputs/reports/`:
```powershell
python generate_reports.py
```

### 5. Launch Interactive Dashboard
Start the Streamlit application:
```powershell
streamlit run app.py
```
Open your browser to: **`http://localhost:8501`**

---

## 7. Data Cleaning & Transformation Pipeline

The data-cleaning pipeline in [src/data_cleaner.py](file:///c:/Users/Shukla/OneDrive/Desktop/PROJECTS/DV/src/data_cleaner.py) strictly enforces non-destructive processing:

| Cleaning Step | Methodology | Impact & Justification |
| :--- | :--- | :--- |
| **Row Pruning** | Drops completely empty rows and trailing padding | Removed 806 empty rows present in raw export. |
| **Integrity Check** | Verifies existence of `Order ID`, `Sales`, `Profit` | Dropped corrupt records lacking critical monetary anchors. |
| **Deduplication** | Identifies identical transactions across all non-ID fields | Removed 1 exact duplicate transaction. |
| **Date Normalization** | Parses dates using mixed format detection | Standardized `Order Date` and `Ship Date` into datetime objects. |
| **Ship Date Guard** | Enforces `Ship Date >= Order Date` | Corrected anomalies where Ship Date preceded Order Date. |
| **Numeric Bounds** | Coerces strings, clips `Sales >= 0`, `Quantity >= 1` | Prevents negative transaction quantities or string values. |
| **Missing Imputation** | Imputes missing postal codes with standard placeholder | Imputed 11 null postal codes without deleting records. |
| **Feature Enrichment**| Derives `Order Year`, `Order Month`, `Shipping Days`, `Profit Margin %`, `Discount Band` | Prepares dimensions for time-series and segment filtering. |

All transformations are tracked and logged in `DataQualityReport`.

---

## 8. Business Metrics & Formulas

To avoid double-counting multi-item orders, metrics adhere strictly to business definitions:

$$\text{Total Sales} = \sum \text{Sales}$$

$$\text{Total Profit} = \sum \text{Profit}$$

$$\text{Profit Margin \%} = \begin{cases} \left(\frac{\text{Total Profit}}{\text{Total Sales}}\right) \times 100 & \text{if Total Sales} > 0 \\ 0.0\% & \text{otherwise} \end{cases}$$

$$\text{Total Orders} = \text{DISTINCTCOUNT}(\text{Order ID})$$

$$\text{Units Sold} = \sum \text{Quantity}$$

$$\text{Average Order Value (AOV)} = \frac{\text{Total Sales}}{\text{Total Orders}}$$

---

## 9. Dashboard Architecture & User Experience

The dashboard layout features a 6-page navigation system:

1. **🏛️ Executive Overview:** High-level KPI scorecards, monthly time-series trend, category breakdown, regional comparison, and executive brief.
2. **📈 Sales Analysis:** Granular performance across sub-categories and customer segments, sales distribution histogram, and Top 10 revenue drivers.
3. **💰 Profitability Analysis:** Discount vs Profit scatter plot, Sub-category profit bar chart highlighting loss leaders in crimson red, and Top 10 deepest loss products.
4. **🗺️ Geographic Analysis:** US State choropleth map, Top 10 profitable states, and Bottom 10 loss states.
5. **🔍 Data Quality & EDA:** Ingestion audit metrics, descriptive statistics table with quartiles and skewness, Tukey's IQR outlier analysis, plain-English statistical interpretations, and reproducible sampling demonstrator.
6. **💡 Business Insights & Decisions:** Dynamic algorithmic findings with supporting metrics, benchmark comparisons, and actionable management recommendations.

### Interactive Controls
- Dynamic date range filter.
- Multi-select filters for Region, Category, Sub-Category, and Customer Segment.
- Real-time KPI recalculation.
- CSV download buttons for cleaned master data and filtered subsets.

---

## 10. Key Findings from the Actual Dataset

Based on the verified **9,993 transactions ($2.30M revenue, $286.4K profit, 12.47% margin)**:

1. **The Tables Sub-Category Disaster:**
   - **Finding:** While generating **$206,965.53** in gross revenue, the **Tables** sub-category incurred a net loss of **-$17,725.48 (-8.56% margin)**.
   - **Remediation:** Cap promotional discounts on Tables at 10% and renegotiate supplier wholesale pricing.
2. **The 20% Discount Trap:**
   - **Finding:** Orders with discounts exceeding 20% experience severe negative margins. Transactions with discounts above 40% generated **$144,360.29 in sales but produced -$110,610.74 in net losses**.
   - **Remediation:** Remove sales rep autonomy for discounts over 20%; require executive authorization.
3. **Regional Inefficiency in the Central Territory:**
   - **Finding:** The **West Region** leads with an operating margin of **14.94% ($108,418 profit)**, while the **Central Region** lags at only **7.92% ($39,706 profit)** despite comparable sales volume.
   - **Remediation:** Re-evaluate high-freight logistics contracts across Texas and Illinois.
4. **Consumer Segment Foundation:**
   - **Finding:** The **Consumer Segment** represents **50.6% of sales ($1,161,401)** and **46.8% of profit ($134,119)**, forming the core retail foundation.

---

## 11. Power BI Integration

The repository includes complete Power BI materials in `powerbi/`:

- **Data Model:** Normalized Kimball Star Schema with `Fact_Sales` linked (1:N) to `Dim_Date`, `Dim_Product`, `Dim_Customer`, and `Dim_Location`.
- **DAX Library:** 15+ production measures in [powerbi/dax_measures.dax](file:///c:/Users/Shukla/OneDrive/Desktop/PROJECTS/DV/powerbi/dax_measures.dax) (YoY Growth, YTD Sales, Profit Margins, Loss-making ratios).
- **Full Guide:** [powerbi/dashboard_guide.md](file:///c:/Users/Shukla/OneDrive/Desktop/PROJECTS/DV/powerbi/dashboard_guide.md) contains step-by-step instructions for canvas layouts, slicers, cards, decomposition trees, and refresh scheduling.

---

## 12. Automated Testing & Verification Summary

Run the test suite anytime using:
```powershell
python -m pytest -v
```

### Test Coverage (19 Passed Tests):
- `test_load_dataset_csv_string`: CSV parsing from buffer and type detection.
- `test_load_dataset_missing_file`: Proper `FileNotFoundError` handling.
- `test_clean_retail_data_preserves_raw`: Validates non-destructive raw copy preservation.
- `test_clean_retail_data_drops_null_order_id`: Verifies dropping records with missing critical identifiers.
- `test_clean_retail_data_invalid_date_handling`: Checks coercion and handling of invalid date strings.
- `test_clean_retail_data_negative_shipping_days`: Validates ship date >= order date logic.
- `test_clean_retail_data_postal_code_imputation`: Verifies missing postal code imputation.
- `test_clean_retail_data_derived_columns`: Ensures all BI derived columns are computed.
- `test_missing_critical_columns_raises_error`: Validates error reporting for malformed files.
- `test_get_dataset_overview`: Validates metadata and column summary outputs.
- `test_get_descriptive_statistics`: Verifies Mean, Std, Median, Min, Max, and Skewness.
- `test_detect_outliers_iqr`: Tests Tukey's IQR lower and upper fence bounds.
- `test_get_sampling_subsets_reproducibility`: Proves reproducible sampling using fixed random seed (42).
- `test_generate_business_insights`: Validates dynamic insight generation without hardcoding.
- `test_calculate_kpis_basic`: Validates Sales, Profit, Margin, and Distinct Order Counts.
- `test_calculate_kpis_empty_df`: Tests zero division defensive handling for empty inputs.
- `test_calculate_kpis_zero_sales`: Tests zero division defensive handling when sales is zero.
- `test_aggregate_by_dimension`: Tests grouping and aggregation across categorical attributes.
- `test_get_product_rankings`: Validates Top 10 and Bottom 10 leaderboard calculations.

---

## 13. Limitations & Future Roadmap

- **Current Limitations:**
  - Ingestion assumes standard retail transaction schemas (Order, Date, Sales, Profit).
  - Power BI Desktop `.pbix` compilation requires local desktop installation; layout and DAX models are provided for instant import.
- **Future Enhancements:**
  - Multi-currency conversion for cross-border operations.
  - Automated predictive forecasting using Prophet or ARIMA for seasonal Q4 demand planning.
  - Role-based authentication and row-level security (RLS) by regional sales manager.

---

## 14. Academic & Portfolio Submission Notes

- **Author / Analyst:** Senior Data Analyst & BI Engineer
- **Project Scope:** End-to-end Data Ingestion, Automated Cleansing Pipeline, Exploratory Analysis, Metric Engine, Interactive Streamlit BI Dashboard, and Power BI Star Schema Integration.
- **Repository License:** MIT License
