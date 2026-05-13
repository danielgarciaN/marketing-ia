"""
RFM Analysis: Recency, Frequency, Monetary scoring and customer segmentation.
"""
import pandas as pd
import numpy as np


def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate RFM metrics per customer."""
    # Reference date = max date + 1 day
    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum"),
        TotalOrders=("InvoiceNo", "nunique"),
        TotalItems=("Quantity", "sum"),
        AvgOrderValue=("Revenue", lambda x: x.sum() / df.loc[x.index, "InvoiceNo"].nunique()),
        FirstPurchase=("InvoiceDate", "min"),
        LastPurchase=("InvoiceDate", "max"),
        Country=("Country", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "Unknown"),
        UniqueProducts=("StockCode", "nunique"),
    ).reset_index()

    # Recalculate AvgOrderValue properly
    order_totals = df.groupby(["CustomerID", "InvoiceNo"])["Revenue"].sum().reset_index()
    avg_ov = order_totals.groupby("CustomerID")["Revenue"].mean().reset_index()
    avg_ov.columns = ["CustomerID", "AvgOrderValue"]
    rfm = rfm.drop(columns=["AvgOrderValue"]).merge(avg_ov, on="CustomerID")

    rfm["Monetary"] = rfm["Monetary"].round(2)
    rfm["AvgOrderValue"] = rfm["AvgOrderValue"].round(2)

    return rfm


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """Assign R, F, M scores (1-5) using quantiles."""
    # Recency: lower is better, so scoring is reversed.
    rfm["R_Score"] = pd.qcut(rfm["Recency"], q=5, labels=[5, 4, 3, 2, 1], duplicates="drop").astype(int)

    # Frequency: higher is better
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop").astype(int)

    # Monetary: higher is better
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop").astype(int)

    # Combined RFM score
    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
    rfm["RF_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str)

    return rfm


def assign_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """Assign business segments based on RFM scores."""
    def segment(row):
        r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]

        if r >= 4 and f >= 4 and m >= 4:
            return "VIP Customers"
        elif r >= 4 and f >= 3 and m >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "New Customers"
        elif r <= 2 and f >= 3 and m >= 3:
            return "At-Risk Customers"
        elif r <= 2 and f <= 2 and m <= 2:
            return "Lost Customers"
        elif r >= 3 and f >= 2 and m >= 3:
            return "High Potential"
        else:
            return "Occasional Buyers"

    rfm["Segment"] = rfm.apply(segment, axis=1)
    return rfm


def build_rfm_table(df: pd.DataFrame) -> pd.DataFrame:
    """Full RFM pipeline."""
    rfm = calculate_rfm(df)
    rfm = score_rfm(rfm)
    rfm = assign_segments(rfm)
    return rfm
