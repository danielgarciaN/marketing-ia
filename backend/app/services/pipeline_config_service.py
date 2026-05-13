"""Pipeline configuration persistence for dataset mapping and RFM settings."""
import copy
import json
import os
from typing import Any

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "pipeline_config.json")

CANONICAL_FIELDS = {
    "invoice_id": "InvoiceNo",
    "product_id": "StockCode",
    "description": "Description",
    "quantity": "Quantity",
    "invoice_date": "InvoiceDate",
    "unit_price": "UnitPrice",
    "customer_id": "CustomerID",
    "country": "Country",
    "revenue": "Revenue",
}

REQUIRED_CANONICAL_FIELDS = [
    "invoice_id",
    "quantity",
    "invoice_date",
    "customer_id",
]

DEFAULT_CONFIG: dict[str, Any] = {
    "source": {
        "filename": "online_retail.csv",
        "source_currency": "GBP",
        "column_mapping": {},
    },
    "rfm": {
        "score_quantiles": 5,
        "weights": {
            "recency": 1.0,
            "frequency": 1.0,
            "monetary": 1.0,
        },
        "active_days": 30,
        "inactive_days": 180,
        "new_customer_max_frequency": 2,
        "segment_thresholds": {
            "vip": {"r": 4, "f": 4, "m": 4},
            "loyal": {"r": 4, "f": 3, "m": 3},
            "at_risk": {"r": 2, "f": 3, "m": 3},
            "lost": {"r": 2, "f": 2, "m": 2},
            "high_potential": {"r": 3, "f": 2, "m": 3},
        },
    },
    "clustering": {
        "n_clusters": 5,
        "auto_select_k": False,
    },
}


def get_default_config() -> dict[str, Any]:
    return copy.deepcopy(DEFAULT_CONFIG)


def load_pipeline_config() -> dict[str, Any]:
    config = get_default_config()
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            stored = json.load(f)
        config = deep_merge(config, stored)
    return config


def save_pipeline_config(config: dict[str, Any]) -> dict[str, Any]:
    current = load_pipeline_config()
    merged = deep_merge(current, config)
    merged = sanitize_config(merged)
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(merged, f, indent=2)
    return merged


def sanitize_config(config: dict[str, Any]) -> dict[str, Any]:
    rfm = config.setdefault("rfm", {})
    weights = rfm.setdefault("weights", {})
    for key in ["recency", "frequency", "monetary"]:
        weights[key] = _bounded_float(weights.get(key, 1.0), 0.0, 5.0, 1.0)

    rfm["score_quantiles"] = int(_bounded_float(rfm.get("score_quantiles", 5), 3, 10, 5))
    rfm["active_days"] = int(_bounded_float(rfm.get("active_days", 30), 1, 3650, 30))
    rfm["inactive_days"] = int(_bounded_float(rfm.get("inactive_days", 180), 1, 3650, 180))
    rfm["new_customer_max_frequency"] = int(_bounded_float(rfm.get("new_customer_max_frequency", 2), 1, 50, 2))

    clustering = config.setdefault("clustering", {})
    clustering["n_clusters"] = int(_bounded_float(clustering.get("n_clusters", 5), 2, 12, 5))
    clustering["auto_select_k"] = bool(clustering.get("auto_select_k", False))

    source = config.setdefault("source", {})
    source["source_currency"] = str(source.get("source_currency", "GBP")).upper()
    source.setdefault("column_mapping", {})
    source.setdefault("filename", "online_retail.csv")
    return config


def deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(base)
    for key, value in (update or {}).items():
        if isinstance(value, dict) and isinstance(output.get(key), dict):
            output[key] = deep_merge(output[key], value)
        else:
            output[key] = value
    return output


def _bounded_float(value: Any, minimum: float, maximum: float, fallback: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return fallback
    return max(minimum, min(maximum, number))
