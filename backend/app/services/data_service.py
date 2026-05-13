"""
Data service: loads processed data into memory for API use.
"""
import pandas as pd
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


class DataService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def load(self):
        if self._loaded:
            return
        self.customers = pd.read_csv(os.path.join(DATA_DIR, "customers_rfm.csv"))
        self.transactions = pd.read_csv(
            os.path.join(DATA_DIR, "online_retail_clean.csv"),
            parse_dates=["InvoiceDate"]
        )

        with open(os.path.join(DATA_DIR, "dashboard_summary.json")) as f:
            self.dashboard_summary = json.load(f)

        with open(os.path.join(DATA_DIR, "revenue_monthly.json")) as f:
            self.revenue_monthly = json.load(f)

        with open(os.path.join(DATA_DIR, "segment_summary.json")) as f:
            self.segment_summary = json.load(f)

        with open(os.path.join(DATA_DIR, "cluster_interpretations.json")) as f:
            self.cluster_interpretations = json.load(f)

        with open(os.path.join(DATA_DIR, "model_metrics.json")) as f:
            self.model_metrics = json.load(f)

        self._loaded = True

    def get_customer(self, customer_id: int) -> dict:
        row = self.customers[self.customers["CustomerID"] == customer_id]
        if row.empty:
            return None
        return row.iloc[0].to_dict()

    def get_customers_by_segment(self, segment: str) -> list:
        filtered = self.customers[self.customers["Segment"] == segment]
        return filtered.to_dict(orient="records")

    def get_segment_names(self) -> list:
        return sorted(self.customers["Segment"].unique().tolist())


data_service = DataService()
