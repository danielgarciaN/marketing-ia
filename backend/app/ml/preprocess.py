"""Data preprocessing: cleaning, validation and feature creation."""
import os

import pandas as pd

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "online_retail.csv")
PROCESSED_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "online_retail_clean.csv")


def load_raw_data(path: str = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["InvoiceDate"])


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw transaction data."""
    initial = len(df)

    df = df.dropna(subset=["CustomerID"]).copy()
    df["CustomerID"] = df["CustomerID"].astype(int)

    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df = df.drop_duplicates()

    df["Revenue"] = (df["Quantity"] * df["UnitPrice"]).round(2)
    df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["InvoiceDay"] = df["InvoiceDate"].dt.date

    cleaned = len(df)
    print(f"Cleaning: {initial} -> {cleaned} rows ({initial - cleaned} removed)")

    return df.reset_index(drop=True)


def save_processed(df: pd.DataFrame, path: str = PROCESSED_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved processed data to {path} ({len(df)} rows)")


if __name__ == "__main__":
    data = load_raw_data()
    data = clean_data(data)
    save_processed(data)
    print("\nProcessed dataset:")
    print(f"  Rows: {len(data)}")
    print(f"  Customers: {data['CustomerID'].nunique()}")
    print(f"  Revenue: GBP {data['Revenue'].sum():,.2f}")
    print(f"  Date range: {data['InvoiceDate'].min()} - {data['InvoiceDate'].max()}")
