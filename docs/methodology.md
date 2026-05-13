# Methodology

## 1. Data Cleaning

The raw transaction dataset is cleaned by:

- Dropping rows with missing `CustomerID`.
- Removing cancelled invoices where `InvoiceNo` starts with `C`.
- Removing zero or negative quantities and prices.
- Removing duplicates.
- Creating `Revenue = Quantity * UnitPrice`.
- Extracting month and day fields for dashboard aggregation.

## 2. RFM Analysis

Each customer receives:

- `Recency`: days since last purchase.
- `Frequency`: number of unique invoices.
- `Monetary`: total customer revenue.
- `AvgOrderValue`: average order value.
- `R_Score`, `F_Score`, `M_Score`: quantile-based scores from 1 to 5.

Business segments are created with rule-based logic so they are explainable to marketing stakeholders.

## 3. Clustering

The clustering pipeline uses:

- Log transform for skewed Frequency and Monetary values.
- StandardScaler.
- KMeans.
- Silhouette score and inertia across k values.
- PCA with two components for visualization.

The current MVP trains a 5-cluster model and exports model artifacts with Joblib.

## 4. Recommendations and Insights

Campaign recommendations are mapped to business segments. Insights are generated through deterministic rules that translate segment statistics and revenue trends into marketing actions.

This keeps the MVP reproducible without requiring external LLM credentials. An LLM layer can be added later to rewrite or enrich the final narratives.
