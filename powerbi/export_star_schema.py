"""
Star Schema Generator for Power BI Deliverable
==============================================
Transforms the flat cleaned Superstore dataset into a normalized Kimball Star Schema:
- Fact_Sales: Granular transaction records with foreign keys and measures.
- Dim_Product: Product hierarchy (Product ID, Product Name, Category, Sub-Category).
- Dim_Customer: Customer details (Customer ID, Customer Name, Segment).
- Dim_Location: Geographic attributes (Postal Code, City, State, Region, Country).
- Dim_Date: Continuous calendar table with fiscal/quarterly attributes.
"""

from pathlib import Path
import pandas as pd


def generate_star_schema(cleaned_csv_path: str, output_dir: str):
    df = pd.read_csv(cleaned_csv_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # 1. Dim_Product
    dim_product = df[["Product ID", "Product Name", "Category", "Sub-Category"]].drop_duplicates(subset=["Product ID"]).reset_index(drop=True)
    dim_product.to_csv(out / "Dim_Product.csv", index=False)

    # 2. Dim_Customer
    dim_customer = df[["Customer ID", "Customer Name", "Segment"]].drop_duplicates(subset=["Customer ID"]).reset_index(drop=True)
    dim_customer.to_csv(out / "Dim_Customer.csv", index=False)

    # 3. Dim_Location
    # Create surrogate Location Key
    loc_cols = ["Postal Code", "City", "State", "Region", "Country"]
    dim_location = df[loc_cols].drop_duplicates().reset_index(drop=True)
    dim_location["Location_Key"] = dim_location.index + 1
    dim_location.to_csv(out / "Dim_Location.csv", index=False)

    # 4. Dim_Date
    min_date = df["Order Date"].min()
    max_date = df["Order Date"].max()
    all_dates = pd.date_range(min_date, max_date, freq="D")
    dim_date = pd.DataFrame({"Date": all_dates})
    dim_date["Year"] = dim_date["Date"].dt.year
    dim_date["Month"] = dim_date["Date"].dt.month
    dim_date["Month_Name"] = dim_date["Date"].dt.strftime("%B")
    dim_date["Month_Short"] = dim_date["Date"].dt.strftime("%b")
    dim_date["Year_Month"] = dim_date["Date"].dt.strftime("%Y-%m")
    dim_date["Quarter"] = "Q" + dim_date["Date"].dt.quarter.astype(str)
    dim_date["Year_Quarter"] = dim_date["Year"].astype(str) + " " + dim_date["Quarter"]
    dim_date["Day_Of_Week"] = dim_date["Date"].dt.day_name()
    dim_date["Is_Weekend"] = dim_date["Date"].dt.dayofweek.isin([5, 6]).astype(int)
    dim_date.to_csv(out / "Dim_Date.csv", index=False)

    # 5. Fact_Sales
    # Merge Location Key
    fact_sales = df.merge(dim_location, on=loc_cols, how="left")
    fact_cols = [
        "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Product ID", "Location_Key",
        "Sales", "Quantity", "Discount", "Profit", "Shipping Days"
    ]
    fact_sales = fact_sales[fact_cols]
    fact_sales.to_csv(out / "Fact_Sales.csv", index=False)

    print(f"Star schema tables successfully generated in: {out}")
    print(f"- Fact_Sales: {len(fact_sales):,} rows")
    print(f"- Dim_Product: {len(dim_product):,} rows")
    print(f"- Dim_Customer: {len(dim_customer):,} rows")
    print(f"- Dim_Location: {len(dim_location):,} rows")
    print(f"- Dim_Date: {len(dim_date):,} rows")


if __name__ == "__main__":
    generate_star_schema("data/processed/cleaned_superstore.csv", "powerbi/star_schema")
