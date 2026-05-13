"""Dataset upload and retraining endpoints."""
from io import BytesIO
import os

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.ml.preprocess import RAW_PATH
from app.ml.train_model import run_pipeline
from app.services.data_service import DATA_DIR, data_service

router = APIRouter(prefix="/data", tags=["Data"])

REQUIRED_COLUMNS = {
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
}


@router.get("/status")
def get_data_status():
    raw_info = _file_info(RAW_PATH)
    processed_path = os.path.join(DATA_DIR, "customers_rfm.csv")
    processed_info = _file_info(processed_path)

    status = {
        "raw_dataset": raw_info,
        "processed_customers": processed_info,
        "required_columns": sorted(REQUIRED_COLUMNS),
        "loaded_in_memory": data_service._loaded,
    }

    if os.path.exists(processed_path):
        customers = pd.read_csv(processed_path, usecols=["CustomerID", "Segment"])
        status["customer_count"] = int(customers["CustomerID"].nunique())
        status["segments"] = sorted(customers["Segment"].dropna().unique().tolist())

    return status


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), retrain: bool = Form(True)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        preview = pd.read_csv(BytesIO(content), nrows=100)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}") from exc

    missing = sorted(REQUIRED_COLUMNS - set(preview.columns))
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Dataset is missing required columns.",
                "missing_columns": missing,
                "required_columns": sorted(REQUIRED_COLUMNS),
            },
        )

    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    with open(RAW_PATH, "wb") as f:
        f.write(content)

    result = {
        "status": "uploaded",
        "filename": file.filename,
        "bytes": len(content),
        "raw_path": RAW_PATH,
        "retrained": False,
    }

    if retrain:
        result["training"] = _run_training()
        result["retrained"] = True

    return result


@router.post("/retrain")
def retrain_dataset():
    if not os.path.exists(RAW_PATH):
        raise HTTPException(status_code=404, detail="Raw dataset not found. Upload a CSV first.")
    return {"status": "retrained", "training": _run_training()}


def _run_training():
    try:
        _, _, metrics = run_pipeline()
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
