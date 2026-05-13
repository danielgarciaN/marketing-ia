"""
RFM Analysis: Recency, Frequency, Monetary scoring and customer segmentation.
"""
import pandas as pd


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


DEFAULT_RFM_CONFIG = {
    "score_quantiles": 5,
    "weights": {"recency": 1.0, "frequency": 1.0, "monetary": 1.0},
    "new_customer_max_frequency": 2,
    "segment_thresholds": {
        "vip": {"r": 4, "f": 4, "m": 4},
        "loyal": {"r": 4, "f": 3, "m": 3},
        "at_risk": {"r": 2, "f": 3, "m": 3},
        "lost": {"r": 2, "f": 2, "m": 2},
        "high_potential": {"r": 3, "f": 2, "m": 3},
    },
}


def score_rfm(rfm: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """Assign R, F, M scores (1-5) using quantiles."""
    config = {**DEFAULT_RFM_CONFIG, **(config or {})}
    quantiles = int(config.get("score_quantiles", 5))

    rfm["R_Score"] = _quantile_score(rfm["Recency"], quantiles, higher_is_better=False)
    rfm["F_Score"] = _quantile_score(rfm["Frequency"].rank(method="first"), quantiles, higher_is_better=True)
    rfm["M_Score"] = _quantile_score(rfm["Monetary"].rank(method="first"), quantiles, higher_is_better=True)

    weights = config.get("weights", DEFAULT_RFM_CONFIG["weights"])
    weighted_total = (
        rfm["R_Score"] * float(weights.get("recency", 1.0))
        + rfm["F_Score"] * float(weights.get("frequency", 1.0))
        + rfm["M_Score"] * float(weights.get("monetary", 1.0))
    )

    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
    rfm["Weighted_RFM_Score"] = weighted_total.round(2)
    rfm["RF_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str)

    return rfm


def assign_segments(rfm: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """Assign business segments based on RFM scores."""
    config = {**DEFAULT_RFM_CONFIG, **(config or {})}
    thresholds = config.get("segment_thresholds", DEFAULT_RFM_CONFIG["segment_thresholds"])
    new_frequency = int(config.get("new_customer_max_frequency", 2))

    def segment(row):
        r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]

        vip = thresholds.get("vip", {"r": 4, "f": 4, "m": 4})
        loyal = thresholds.get("loyal", {"r": 4, "f": 3, "m": 3})
        at_risk = thresholds.get("at_risk", {"r": 2, "f": 3, "m": 3})
        lost = thresholds.get("lost", {"r": 2, "f": 2, "m": 2})
        high_potential = thresholds.get("high_potential", {"r": 3, "f": 2, "m": 3})

        if r >= vip["r"] and f >= vip["f"] and m >= vip["m"]:
            return "VIP Customers"
        elif r >= loyal["r"] and f >= loyal["f"] and m >= loyal["m"]:
            return "Loyal Customers"
        elif r >= loyal["r"] and f <= new_frequency:
            return "New Customers"
        elif r <= at_risk["r"] and f >= at_risk["f"] and m >= at_risk["m"]:
            return "At-Risk Customers"
        elif r <= lost["r"] and f <= lost["f"] and m <= lost["m"]:
            return "Lost Customers"
        elif r >= high_potential["r"] and f >= high_potential["f"] and m >= high_potential["m"]:
            return "High Potential"
        else:
            return "Occasional Buyers"

    rfm["Segment"] = rfm.apply(segment, axis=1)
    return rfm


def build_rfm_table(df: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """Full RFM pipeline."""
    rfm = calculate_rfm(df)
    rfm = score_rfm(rfm, config=config)
    rfm = assign_segments(rfm, config=config)
    return rfm


def _quantile_score(series: pd.Series, quantiles: int, higher_is_better: bool) -> pd.Series:
    if series.nunique() <= 1:
        return pd.Series([max(1, quantiles // 2)] * len(series), index=series.index, dtype="int64")

    try:
        raw = pd.qcut(series, q=quantiles, labels=False, duplicates="drop")
    except ValueError:
        raw = pd.cut(series.rank(method="first"), bins=min(quantiles, series.nunique()), labels=False)

    raw = raw.fillna(0).astype(int)
    max_bucket = int(raw.max()) if len(raw) else 0
    if higher_is_better:
        return (raw + 1).clip(1, quantiles).astype(int)
    return (max_bucket - raw + 1).clip(1, quantiles).astype(int)
