"""Model and clustering endpoints."""
from fastapi import APIRouter, Query

from app.services.data_service import data_service

router = APIRouter(prefix="/model", tags=["Model"])


@router.get("/metrics")
def get_model_metrics():
    data_service.load()
    return data_service.model_metrics


@router.get("/clusters")
def get_clusters():
    data_service.load()
    return data_service.cluster_interpretations


@router.get("/cluster-points")
def get_cluster_points(limit: int = Query(500, ge=50, le=5000)):
    data_service.load()
    cols = ["CustomerID", "Segment", "Cluster", "PCA_1", "PCA_2", "Monetary", "Frequency", "Recency"]
    available_cols = [col for col in cols if col in data_service.customers.columns]
    points = data_service.customers[available_cols].head(limit).to_dict(orient="records")
    return {"data": points, "total": int(len(data_service.customers)), "limit": limit}
