# Retail Dataset Quality & Cleansing Audit Report

- **Raw Record Count:** 10,800
- **Cleaned Record Count:** 9,993
- **Records Retained:** 92.53%
- **Completely Blank Rows Dropped:** 0
- **Duplicate Transactions Dropped:** 1
- **Missing Key Monetary Records Handled:** 806
- **Date Range:** 2015-01-03 to 2018-12-30

### Data Quality Transformation Actions

- Removed 806 records with missing Order ID, Sales, or Profit.
- Removed 1 duplicate transaction records.

### Imputed Fields

- **Postal Code:** Imputed 11 missing postal codes with '99999'.
