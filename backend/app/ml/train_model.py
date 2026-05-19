"""Full training pipeline: preprocess -> RFM -> clustering -> save results."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.ml.clustering import run_clustering_pipeline
from app.ml.preprocess import clean_data, load_raw_data, save_processed
from app.ml.rfm import build_rfm_table
from app.services.pipeline_config_service import load_pipeline_config

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def run_pipeline(config: dict | None = None):
    config = config or load_pipeline_config()
    rfm_config = config.get("rfm", {})
    clustering_config = config.get("clustering", {})

    print("=" * 60)
    print("AI Marketing Intelligence Platform - Training Pipeline")
    print("=" * 60)

    print("\nStep 1: Loading and cleaning data...")
    df = load_raw_data()
    df = clean_data(df)
    if df.empty:
        print("  No active rows found. Writing empty processed outputs.")
        write_empty_outputs(config)
        return df, {}, {"n_clusters": 0, "silhouette_score": 0, "inertia": 0, "eval_results": {"k": [], "silhouette": [], "inertia": []}}
    save_processed(df)

    print("\nStep 2: Building RFM table...")
    rfm = build_rfm_table(df, config=rfm_config)
    print(f"  RFM table: {len(rfm)} customers")
    print(f"  Segments: {rfm['Segment'].value_counts().to_dict()}")

    print("\nStep 3: Running clustering pipeline...")
    n_clusters = None if clustering_config.get("auto_select_k") else clustering_config.get("n_clusters", 5)
    rfm, interpretations, metrics = run_clustering_pipeline(rfm, n_clusters=n_clusters)
    print(f"  Clusters: {rfm['Cluster'].value_counts().sort_index().to_dict()}")
    print(f"  Silhouette Score: {metrics['silhouette_score']}")

    print("\nStep 4: Saving results...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    customer_path = os.path.join(PROCESSED_DIR, "customers_rfm.csv")
    rfm.to_csv(customer_path, index=False)
    print(f"  Customers RFM -> {customer_path}")

    interp_path = os.path.join(PROCESSED_DIR, "cluster_interpretations.json")
    with open(interp_path, "w") as f:
        json.dump(interpretations, f, indent=2)
    print(f"  Cluster interpretations -> {interp_path}")

    metrics_out = {k: v for k, v in metrics.items() if k != "eval_results"}
    metrics_out["eval_k"] = metrics["eval_results"]["k"]
    metrics_out["eval_silhouette"] = metrics["eval_results"]["silhouette"]
    metrics_out["eval_inertia"] = metrics["eval_results"]["inertia"]
    metrics_out["rfm_config"] = rfm_config
    metrics_out["clustering_config"] = clustering_config

    metrics_path = os.path.join(PROCESSED_DIR, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics_out, f, indent=2)
    print(f"  Model metrics -> {metrics_path}")

    dashboard = {
        "total_customers": int(rfm["CustomerID"].nunique()),
        "total_revenue": round(float(df["Revenue"].sum()), 2),
        "total_orders": int(df["InvoiceNo"].nunique()),
        "avg_order_value": round(float(df.groupby("InvoiceNo")["Revenue"].sum().mean()), 2),
        "avg_frequency": round(float(rfm["Frequency"].mean()), 2),
        "active_customers": int((rfm["Recency"] <= rfm_config.get("active_days", 30)).sum()),
        "inactive_customers": int((rfm["Recency"] > rfm_config.get("inactive_days", 180)).sum()),
        "top_country": df["Country"].mode().iloc[0],
        "source_currency": config.get("source", {}).get("source_currency", "GBP"),
        "rfm_weights": rfm_config.get("weights", {}),
        "date_range": {
            "start": str(df["InvoiceDate"].min().date()),
            "end": str(df["InvoiceDate"].max().date()),
        },
    }
    dash_path = os.path.join(PROCESSED_DIR, "dashboard_summary.json")
    with open(dash_path, "w") as f:
        json.dump(dashboard, f, indent=2)
    print(f"  Dashboard summary -> {dash_path}")

    revenue_monthly = (
        df.groupby("InvoiceMonth")["Revenue"]
        .sum()
        .round(2)
        .reset_index()
        .rename(columns={"InvoiceMonth": "month", "Revenue": "revenue"})
        .to_dict(orient="records")
    )
    rev_path = os.path.join(PROCESSED_DIR, "revenue_monthly.json")
    with open(rev_path, "w") as f:
        json.dump(revenue_monthly, f, indent=2)
    print(f"  Revenue monthly -> {rev_path}")

    seg_summary = []
    for seg_name, group in rfm.groupby("Segment"):
        seg_summary.append(
            {
                "segment": seg_name,
                "count": int(len(group)),
                "total_revenue": round(float(group["Monetary"].sum()), 2),
                "avg_monetary": round(float(group["Monetary"].mean()), 2),
                "avg_frequency": round(float(group["Frequency"].mean()), 2),
                "avg_recency": round(float(group["Recency"].mean()), 2),
                "avg_order_value": round(float(group["AvgOrderValue"].mean()), 2),
                "pct_revenue": round(float(group["Monetary"].sum() / rfm["Monetary"].sum() * 100), 1),
                "pct_customers": round(float(len(group) / len(rfm) * 100), 1),
            }
        )
    seg_path = os.path.join(PROCESSED_DIR, "segment_summary.json")
    with open(seg_path, "w") as f:
        json.dump(seg_summary, f, indent=2)
    print(f"  Segment summary -> {seg_path}")

    print("\nPipeline complete!")
    return rfm, interpretations, metrics


def write_empty_outputs(config: dict | None = None):
    config = config or load_pipeline_config()
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    empty_transactions = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
        "Revenue",
        "InvoiceMonth",
        "InvoiceDay",
    ]
    empty_customers = [
        "CustomerID",
        "Recency",
        "Frequency",
        "Monetary",
        "TotalOrders",
        "TotalItems",
        "FirstPurchase",
        "LastPurchase",
        "Country",
        "UniqueProducts",
        "AvgOrderValue",
        "R_Score",
        "F_Score",
        "M_Score",
        "RFM_Score",
        "Weighted_RFM_Score",
        "RF_Score",
        "Segment",
        "Cluster",
        "PCA_1",
        "PCA_2",
    ]

    import pandas as pd

    pd.DataFrame(columns=empty_transactions).to_csv(os.path.join(PROCESSED_DIR, "online_retail_clean.csv"), index=False)
    pd.DataFrame(columns=empty_customers).to_csv(os.path.join(PROCESSED_DIR, "customers_rfm.csv"), index=False)

    dashboard = {
        "total_customers": 0,
        "total_revenue": 0,
        "total_orders": 0,
        "avg_order_value": 0,
        "avg_frequency": 0,
        "active_customers": 0,
        "inactive_customers": 0,
        "top_country": "Not available",
        "source_currency": config.get("source", {}).get("source_currency", "GBP"),
        "rfm_weights": config.get("rfm", {}).get("weights", {}),
        "date_range": {"start": None, "end": None},
    }

    outputs = {
        "dashboard_summary.json": dashboard,
        "revenue_monthly.json": [],
        "segment_summary.json": [],
        "cluster_interpretations.json": {},
        "model_metrics.json": {
            "n_clusters": 0,
            "silhouette_score": 0,
            "inertia": 0,
            "eval_k": [],
            "eval_silhouette": [],
            "eval_inertia": [],
            "rfm_config": config.get("rfm", {}),
            "clustering_config": config.get("clustering", {}),
        },
    }

    for filename, payload in outputs.items():
        with open(os.path.join(PROCESSED_DIR, filename), "w") as f:
            json.dump(payload, f, indent=2)


if __name__ == "__main__":
    run_pipeline()
