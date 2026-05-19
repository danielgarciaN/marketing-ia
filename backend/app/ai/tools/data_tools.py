"""Data access tools — thin wrappers over the existing DataService."""
from typing import Any
from langchain_core.tools import tool

from app.services.data_service import DataService


def _svc() -> DataService:
    svc = DataService()
    svc.load()
    return svc


@tool
def get_dashboard_summary() -> dict[str, Any]:
    """Return high-level KPI summary: total customers, revenue, orders, active/inactive ratio."""
    svc = _svc()
    return svc.dashboard_summary or {}


@tool
def get_customer_by_id(customer_id: str) -> dict[str, Any]:
    """Retrieve full profile for a single customer: RFM scores, segment, cluster, spend history."""
    svc = _svc()
    customer = svc.get_customer(customer_id)
    if customer is None:
        return {"error": f"Customer '{customer_id}' not found."}
    return customer.to_dict() if hasattr(customer, "to_dict") else dict(customer)


@tool
def get_customers_by_segment(segment: str, limit: int = 50) -> list[dict[str, Any]]:
    """Return customers belonging to a named RFM segment (e.g. 'VIP Customers', 'At-Risk').
    Use limit to control how many rows to return (max 500).
    """
    svc = _svc()
    limit = min(limit, 500)
    customers = svc.get_customers_by_segment(segment)
    if customers is None or len(customers) == 0:
        return []
    return customers.head(limit).to_dict(orient="records")


@tool
def get_segment_overview() -> list[dict[str, Any]]:
    """Return aggregated statistics for every RFM segment: count, revenue share, avg RFM scores."""
    svc = _svc()
    if svc.segment_summary is None:
        return []
    if hasattr(svc.segment_summary, "to_dict"):
        return svc.segment_summary.to_dict(orient="records")
    if isinstance(svc.segment_summary, list):
        return svc.segment_summary
    return []
