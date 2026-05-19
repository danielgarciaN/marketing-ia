"""File-backed dataset registry prepared for future database persistence."""
from __future__ import annotations

import json
import os
import shutil
import uuid
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from app.services.pipeline_config_service import CANONICAL_FIELDS

DATA_ROOT = os.path.join(os.path.dirname(__file__), "..", "data")
DATASETS_DIR = os.path.join(DATA_ROOT, "datasets")
REGISTRY_PATH = os.path.join(DATASETS_DIR, "datasets_registry.json")
RAW_PATH = os.path.join(DATA_ROOT, "raw", "online_retail.csv")

CANONICAL_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
    "Revenue",
]


def ensure_registry() -> list[dict[str, Any]]:
    os.makedirs(DATASETS_DIR, exist_ok=True)
    if not os.path.exists(REGISTRY_PATH):
        _write_registry([])
    return _read_registry()


def list_datasets() -> list[dict[str, Any]]:
    datasets = ensure_registry()
    return sorted(datasets, key=lambda item: item.get("uploaded_at", ""), reverse=True)


def add_dataset(
    *,
    filename: str,
    content: bytes,
    normalized: pd.DataFrame,
    file_type: str,
    mapping: dict[str, str],
    confidence: dict[str, float],
    quality: dict[str, Any],
    source_currency: str,
    active: bool = True,
) -> dict[str, Any]:
    datasets = ensure_registry()
    dataset_id = uuid.uuid4().hex[:12]
    dataset_dir = os.path.join(DATASETS_DIR, dataset_id)
    os.makedirs(dataset_dir, exist_ok=True)

    safe_name = _safe_filename(filename)
    original_path = os.path.join(dataset_dir, safe_name)
    normalized_path = os.path.join(dataset_dir, "normalized.csv")

    with open(original_path, "wb") as f:
        f.write(content)
    normalized.to_csv(normalized_path, index=False)

    stats = dataset_stats(normalized)
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "id": dataset_id,
        "filename": filename,
        "file_type": file_type,
        "active": active,
        "uploaded_at": now,
        "updated_at": now,
        "size_bytes": len(content),
        "original_path": original_path,
        "normalized_path": normalized_path,
        "source_currency": source_currency,
        "mapping": mapping,
        "confidence": confidence,
        "quality": quality,
        "stats": stats,
    }
    datasets.append(record)
    _write_registry(datasets)
    return record


def set_dataset_active(dataset_id: str, active: bool) -> dict[str, Any]:
    datasets = ensure_registry()
    for item in datasets:
        if item["id"] == dataset_id:
            item["active"] = active
            item["updated_at"] = datetime.now(timezone.utc).isoformat()
            _write_registry(datasets)
            return item
    raise KeyError(dataset_id)


def delete_dataset(dataset_id: str) -> dict[str, Any]:
    datasets = ensure_registry()
    removed = next((item for item in datasets if item["id"] == dataset_id), None)
    if not removed:
        raise KeyError(dataset_id)
    remaining = [item for item in datasets if item["id"] != dataset_id]
    _write_registry(remaining)

    dataset_dir = os.path.join(DATASETS_DIR, dataset_id)
    if os.path.abspath(dataset_dir).startswith(os.path.abspath(DATASETS_DIR)) and os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)

    return removed


def build_active_raw_dataset() -> dict[str, Any]:
    datasets = ensure_registry()
    active = [item for item in datasets if item.get("active")]
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

    if not active:
        pd.DataFrame(columns=CANONICAL_COLUMNS).to_csv(RAW_PATH, index=False)
        return {"active_dataset_count": 0, "rows": 0, "raw_path": RAW_PATH}

    frames = []
    for item in active:
        path = item.get("normalized_path")
        if path and os.path.exists(path):
            frames.append(pd.read_csv(path))

    if not frames:
        pd.DataFrame(columns=CANONICAL_COLUMNS).to_csv(RAW_PATH, index=False)
        return {"active_dataset_count": 0, "rows": 0, "raw_path": RAW_PATH}

    combined = pd.concat(frames, ignore_index=True)
    for column in CANONICAL_COLUMNS:
        if column not in combined.columns:
            combined[column] = "" if column in {"StockCode", "Description", "Country"} else 0
    combined[CANONICAL_COLUMNS].to_csv(RAW_PATH, index=False)
    return {"active_dataset_count": len(active), "rows": int(len(combined)), "raw_path": RAW_PATH}


def dataset_stats(df: pd.DataFrame) -> dict[str, Any]:
    revenue = _revenue_series(df)
    output = {
        "rows": int(len(df)),
        "customers": int(df["CustomerID"].nunique()) if "CustomerID" in df.columns else 0,
        "orders": int(df["InvoiceNo"].nunique()) if "InvoiceNo" in df.columns else 0,
        "revenue": round(float(revenue.fillna(0).sum()), 2),
        "date_start": None,
        "date_end": None,
    }
    if "InvoiceDate" in df.columns and len(df):
        dates = pd.to_datetime(df["InvoiceDate"], errors="coerce").dropna()
        if not dates.empty:
            output["date_start"] = str(dates.min().date())
            output["date_end"] = str(dates.max().date())
    return output


def _revenue_series(df: pd.DataFrame) -> pd.Series:
    if "Revenue" in df.columns:
        return pd.to_numeric(df["Revenue"], errors="coerce")
    if "Quantity" in df.columns and "UnitPrice" in df.columns:
        quantity = pd.to_numeric(df["Quantity"], errors="coerce")
        price = pd.to_numeric(df["UnitPrice"], errors="coerce")
        return quantity * price
    return pd.Series([0] * len(df))


def registry_summary() -> dict[str, Any]:
    datasets = list_datasets()
    active = [item for item in datasets if item.get("active")]
    return {
        "datasets": datasets,
        "total_datasets": len(datasets),
        "active_datasets": len(active),
        "active_rows": sum(int(item.get("stats", {}).get("rows", 0)) for item in active),
        "active_customers": sum(int(item.get("stats", {}).get("customers", 0)) for item in active),
        "active_revenue": round(sum(float(item.get("stats", {}).get("revenue", 0)) for item in active), 2),
    }


def bootstrap_default_dataset() -> None:
    datasets = ensure_registry()
    if datasets or not os.path.exists(RAW_PATH):
        return
    df = pd.read_csv(RAW_PATH)
    content = df.to_csv(index=False).encode("utf-8")
    mapping = {field: target for field, target in CANONICAL_FIELDS.items() if target in df.columns}
    add_dataset(
        filename="online_retail.csv",
        content=content,
        normalized=df,
        file_type="csv",
        mapping=mapping,
        confidence={field: 1.0 for field in mapping},
        quality={"rows": int(len(df)), "columns": int(len(df.columns)), "warnings": []},
        source_currency="GBP",
        active=True,
    )


def _read_registry() -> list[dict[str, Any]]:
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def _write_registry(datasets: list[dict[str, Any]]) -> None:
    os.makedirs(DATASETS_DIR, exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(datasets, f, indent=2)


def _safe_filename(filename: str) -> str:
    keep = [char if char.isalnum() or char in {".", "-", "_"} else "_" for char in filename]
    cleaned = "".join(keep).strip("._")
    return cleaned or "dataset.csv"
