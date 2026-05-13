"""Customer endpoints."""
from fastapi import APIRouter, HTTPException, Query
from app.services.data_service import data_service
import math

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("")
def get_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=10, le=200),
    segment: str = Query(None),
    cluster: int = Query(None),
    sort_by: str = Query("Monetary"),
    sort_desc: bool = Query(True),
    search: str = Query(None),
):
    data_service.load()
    df = data_service.customers.copy()

    # Filters
    if segment:
        df = df[df["Segment"] == segment]
    if cluster is not None:
        df = df[df["Cluster"] == cluster]
    if search:
        df = df[df["CustomerID"].astype(str).str.contains(search)]

    # Sort
    if sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=not sort_desc)

    total = len(df)
    total_pages = math.ceil(total / page_size)
    start = (page - 1) * page_size

    cols = ["CustomerID", "Country", "Recency", "Frequency", "Monetary",
            "AvgOrderValue", "R_Score", "F_Score", "M_Score", "RFM_Score",
            "Segment", "Cluster"]
    available_cols = [c for c in cols if c in df.columns]

    records = df.iloc[start:start + page_size][available_cols].to_dict(orient="records")

    return {
        "data": records,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    data_service.load()
    result = data_service.get_customer(customer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    # Clean NaN values
    return {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in result.items()}
