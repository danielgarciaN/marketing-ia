"""Dataset upload, schema inference, configurable mapping and retraining endpoints."""
from io import BytesIO
import json
import os
import re
import zlib
from typing import Any

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.ml.preprocess import RAW_PATH
from app.ml.train_model import run_pipeline
from app.services.data_service import DATA_DIR, data_service
from app.services.dataset_registry_service import (
    add_dataset,
    bootstrap_default_dataset,
    build_active_raw_dataset,
    delete_dataset,
    registry_summary,
    set_dataset_active,
)
from app.services.pipeline_config_service import (
    CANONICAL_FIELDS,
    REQUIRED_CANONICAL_FIELDS,
    deep_merge,
    load_pipeline_config,
    save_pipeline_config,
)

router = APIRouter(prefix="/data", tags=["Data"])

FIELD_LABELS = {
    "invoice_id": "Invoice ID",
    "product_id": "Product ID",
    "description": "Product description",
    "quantity": "Quantity",
    "invoice_date": "Invoice date",
    "unit_price": "Unit price",
    "customer_id": "Customer ID",
    "country": "Country",
    "revenue": "Revenue",
}

FIELD_SYNONYMS = {
    "invoice_id": ["invoiceno", "invoice", "invoiceid", "orderid", "ordernumber", "order", "transactionid", "transaction"],
    "product_id": ["stockcode", "sku", "productid", "productcode", "itemid", "variantid"],
    "description": ["description", "productname", "product", "itemname", "title", "name"],
    "quantity": ["quantity", "qty", "units", "items", "itemquantity", "lineitemquantity", "unitsbought", "unitsordered"],
    "invoice_date": ["invoicedate", "date", "orderdate", "createdat", "created", "timestamp", "purchasedate"],
    "unit_price": ["unitprice", "price", "unitcost", "itemprice", "lineprice", "amount", "subtotal", "priceeach"],
    "customer_id": ["customerid", "customer", "userid", "buyerid", "clientid", "email", "customeremail", "clientidentifier", "customeridentifier"],
    "country": ["country", "billingcountry", "shippingcountry", "market", "region", "marketcountry"],
    "revenue": ["revenue", "sales", "total", "totalprice", "ordertotal", "lineitemtotal", "grosssales", "netrevenue", "totalpaid", "totalspent"],
}


@router.get("/status")
def get_data_status():
    bootstrap_default_dataset()
    raw_info = _file_info(RAW_PATH)
    processed_path = os.path.join(DATA_DIR, "customers_rfm.csv")
    processed_info = _file_info(processed_path)
    config = load_pipeline_config()

    status = {
        "raw_dataset": raw_info,
        "processed_customers": processed_info,
        "required_fields": _field_metadata(),
        "required_columns": sorted(CANONICAL_FIELDS.values()),
        "config": config,
        "dataset_registry": registry_summary(),
        "loaded_in_memory": data_service._loaded,
    }

    if os.path.exists(processed_path):
        customers = pd.read_csv(processed_path, usecols=["CustomerID", "Segment"])
        status["customer_count"] = int(customers["CustomerID"].nunique())
        status["segments"] = sorted(customers["Segment"].dropna().unique().tolist())

    return status


@router.get("/datasets")
def get_datasets():
    bootstrap_default_dataset()
    return registry_summary()


@router.post("/datasets/{dataset_id}/activate")
def activate_dataset(dataset_id: str, payload: dict[str, Any]):
    try:
        dataset = set_dataset_active(dataset_id, bool(payload.get("active", True)))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Dataset not found.") from exc

    config = load_pipeline_config()
    build_result = build_active_raw_dataset()
    training = _run_training(config)
    return {"dataset": dataset, "build": build_result, "training": training, "registry": registry_summary()}


@router.delete("/datasets/{dataset_id}")
def remove_dataset(dataset_id: str):
    try:
        dataset = delete_dataset(dataset_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Dataset not found.") from exc

    config = load_pipeline_config()
    build_result = build_active_raw_dataset()
    training = _run_training(config)
    return {"deleted": dataset, "build": build_result, "training": training, "registry": registry_summary()}


@router.get("/config")
def get_config():
    return load_pipeline_config()


@router.post("/config")
async def update_config(payload: dict[str, Any]):
    return save_pipeline_config(payload)


@router.post("/infer-schema")
async def infer_schema(file: UploadFile = File(...)):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    df = _read_tabular_file(content, file.filename, preview_only=True)
    inference = _infer_mapping(df)
    quality = _profile_dataframe(df, inference["mapping"])
    missing = _missing_fields(inference["mapping"])
    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "sample_rows": df.head(5).fillna("").to_dict(orient="records"),
        "mapping": inference["mapping"],
        "confidence": inference["confidence"],
        "missing_fields": missing,
        "field_metadata": _field_metadata(),
        "quality": quality,
        "needs_manual_review": bool(missing or _low_confidence_fields(inference["confidence"])),
        "low_confidence_fields": _low_confidence_fields(inference["confidence"]),
    }


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    retrain: bool = Form(True),
    mapping: str | None = Form(None),
    config: str | None = Form(None),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    df = _read_tabular_file(content, file.filename, preview_only=False)
    inferred = _infer_mapping(df)["mapping"]
    provided_mapping = _parse_json_form(mapping, "mapping") or {}
    column_mapping = {**inferred, **{k: v for k, v in provided_mapping.items() if v}}
    missing = _missing_fields(column_mapping)

    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Dataset mapping is incomplete.",
                "missing_fields": missing,
                "field_metadata": _field_metadata(),
                "inferred_mapping": inferred,
                "available_columns": df.columns.tolist(),
            },
        )

    pipeline_config = load_pipeline_config()
    pipeline_config = _merge_upload_config(pipeline_config, _parse_json_form(config, "config") or {})
    pipeline_config["source"]["filename"] = file.filename
    pipeline_config["source"]["column_mapping"] = column_mapping
    saved_config = save_pipeline_config(pipeline_config)

    normalized = _normalize_dataset(df, column_mapping)
    file_type = file.filename.lower().rsplit(".", 1)[-1] if "." in file.filename else "csv"
    dataset = add_dataset(
        filename=file.filename,
        content=content,
        normalized=normalized,
        file_type=file_type,
        mapping=column_mapping,
        confidence=_infer_mapping(df)["confidence"],
        quality=_profile_dataframe(normalized, {key: CANONICAL_FIELDS[key] for key in CANONICAL_FIELDS}),
        source_currency=saved_config.get("source", {}).get("source_currency", "GBP"),
        active=True,
    )
    build_result = build_active_raw_dataset()

    result = {
        "status": "uploaded",
        "filename": file.filename,
        "rows": int(len(normalized)),
        "bytes": len(content),
        "raw_path": RAW_PATH,
        "dataset": dataset,
        "registry": registry_summary(),
        "active_build": build_result,
        "mapping": column_mapping,
        "config": saved_config,
        "quality": _profile_dataframe(normalized, {key: CANONICAL_FIELDS[key] for key in CANONICAL_FIELDS}),
        "retrained": False,
    }

    if retrain:
        result["training"] = _run_training(saved_config)
        result["retrained"] = True

    return result


@router.post("/retrain")
def retrain_dataset(config: dict[str, Any] | None = None):
    pipeline_config = save_pipeline_config(config or {}) if config else load_pipeline_config()
    bootstrap_default_dataset()
    build_result = build_active_raw_dataset()
    return {"status": "retrained", "config": pipeline_config, "active_build": build_result, "training": _run_training(pipeline_config)}


def _run_training(config: dict[str, Any]):
    try:
        _, _, metrics = run_pipeline(config=config)
        data_service.reset()
        data_service.load()
        return {
            "n_clusters": metrics["n_clusters"],
            "silhouette_score": metrics["silhouette_score"],
            "inertia": metrics["inertia"],
        }
    except Exception as exc:
        data_service.reset()
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc


def _read_tabular_file(content: bytes, filename: str, preview_only: bool) -> pd.DataFrame:
    extension = filename.lower().rsplit(".", 1)[-1] if "." in filename else "csv"
    try:
        if extension in {"xlsx", "xls"}:
            return pd.read_excel(BytesIO(content), nrows=200 if preview_only else None)
        if extension == "csv":
            return pd.read_csv(BytesIO(content), nrows=200 if preview_only else None)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read file: {exc}") from exc

    raise HTTPException(status_code=400, detail="Supported files: CSV, XLSX and XLS.")


def _infer_mapping(df: pd.DataFrame) -> dict[str, Any]:
    columns = df.columns.tolist()
    normalized_columns = {_normalize_name(column): column for column in columns}
    mapping = {}
    confidence = {}

    for field, synonyms in FIELD_SYNONYMS.items():
        match = None
        score = 0.0
        for synonym in synonyms:
            if synonym in normalized_columns:
                match = normalized_columns[synonym]
                score = 1.0
                break
        if match is None:
            match, score = _semantic_match(columns, synonyms)
        if match:
            mapping[field] = match
            confidence[field] = round(score, 2)

    return {"mapping": mapping, "confidence": confidence}


def _semantic_match(columns: list[str], synonyms: list[str]) -> tuple[str | None, float]:
    best_column = None
    best_score = 0.0
    for column in columns:
        normalized = _normalize_name(column)
        for synonym in synonyms:
            if synonym in normalized or normalized in synonym:
                score = min(len(synonym), len(normalized)) / max(len(synonym), len(normalized))
                if score > best_score:
                    best_column = column
                    best_score = max(0.65, score)
    return best_column, best_score


def _low_confidence_fields(confidence: dict[str, float]) -> list[str]:
    return [field for field, score in confidence.items() if score < 0.8]


def _normalize_dataset(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    normalized = pd.DataFrame()
    for field, target in CANONICAL_FIELDS.items():
        source = mapping.get(field)
        if source and source in df.columns:
            normalized[target] = df[source]

    if "Revenue" not in normalized.columns:
        if "UnitPrice" not in normalized.columns:
            raise HTTPException(status_code=400, detail="Mapping needs unit price or revenue.")
        normalized["Revenue"] = pd.to_numeric(normalized["Quantity"], errors="coerce") * pd.to_numeric(normalized["UnitPrice"], errors="coerce")

    if "UnitPrice" not in normalized.columns:
        quantity = pd.to_numeric(normalized["Quantity"], errors="coerce").replace(0, pd.NA)
        normalized["UnitPrice"] = pd.to_numeric(normalized["Revenue"], errors="coerce") / quantity

    normalized["StockCode"] = normalized.get("StockCode", "Unknown")
    normalized["Description"] = normalized.get("Description", "Unknown product")
    normalized["Country"] = normalized.get("Country", "Unknown")
    normalized["InvoiceDate"] = pd.to_datetime(normalized["InvoiceDate"], errors="coerce")
    normalized["CustomerID"] = _normalize_customer_id(normalized["CustomerID"])

    missing_columns = [CANONICAL_FIELDS[field] for field in REQUIRED_CANONICAL_FIELDS if CANONICAL_FIELDS[field] not in normalized.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Normalized dataset is missing columns: {missing_columns}")

    return normalized


def _profile_dataframe(df: pd.DataFrame, mapping: dict[str, str]) -> dict[str, Any]:
    profile = {"rows": int(len(df)), "columns": int(len(df.columns)), "warnings": []}
    for field, column in mapping.items():
        if column not in df.columns:
            continue
        null_pct = float(df[column].isna().mean() * 100) if len(df) else 0.0
        profile[field] = {
            "column": column,
            "null_pct": round(null_pct, 1),
            "dtype": str(df[column].dtype),
        }
        if null_pct > 10:
            profile["warnings"].append(f"{FIELD_LABELS.get(field, field)} has {null_pct:.1f}% missing values.")

    date_column = mapping.get("invoice_date")
    if date_column and date_column in df.columns:
        parsed = pd.to_datetime(df[date_column], errors="coerce")
        invalid_pct = float(parsed.isna().mean() * 100) if len(df) else 0.0
        if invalid_pct > 10:
            profile["warnings"].append(f"Invoice date has {invalid_pct:.1f}% invalid dates.")

    return profile


def _normalize_customer_id(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().all():
        return numeric

    def stable_id(value: Any) -> int | None:
        if pd.isna(value):
            return None
        text = str(value).strip().lower()
        if not text:
            return None
        return int(zlib.crc32(text.encode("utf-8")))

    return series.map(stable_id)


def _missing_fields(mapping: dict[str, str]) -> list[str]:
    missing = [field for field in REQUIRED_CANONICAL_FIELDS if not mapping.get(field)]
    if not mapping.get("unit_price") and not mapping.get("revenue"):
        missing.append("unit_price_or_revenue")
    return missing


def _field_metadata() -> list[dict[str, Any]]:
    fields = []
    for field, target in CANONICAL_FIELDS.items():
        fields.append(
            {
                "field": field,
                "label": FIELD_LABELS[field],
                "target_column": target,
                "required": field in REQUIRED_CANONICAL_FIELDS or field in {"unit_price", "revenue"},
                "synonyms": FIELD_SYNONYMS[field],
            }
        )
    return fields


def _parse_json_form(value: str | None, name: str) -> dict[str, Any] | None:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid {name} JSON.") from exc


def _merge_upload_config(current: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    if not update:
        return current
    return deep_merge(current, update)


def _normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def _file_info(path: str):
    if not os.path.exists(path):
        return {"exists": False}

    stat = os.stat(path)
    return {
        "exists": True,
        "path": path,
        "bytes": stat.st_size,
        "modified_at": stat.st_mtime,
    }
