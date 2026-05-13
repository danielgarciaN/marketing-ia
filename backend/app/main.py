"""AI Marketing Intelligence Platform - API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_campaigns import router as campaigns_router
from app.api.routes_customers import router as customers_router
from app.api.routes_data import router as data_router
from app.api.routes_dashboard import router as dashboard_router
from app.api.routes_insights import router as insights_router
from app.api.routes_model import router as model_router
from app.api.routes_segments import router as segments_router

app = FastAPI(
    title="AI Marketing Intelligence Platform",
    description="Customer Intelligence API: RFM Analysis, Segmentation, Clustering, Campaign Recommendations & Insights",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(data_router)
app.include_router(customers_router)
app.include_router(segments_router)
app.include_router(campaigns_router)
app.include_router(insights_router)
app.include_router(model_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "name": "AI Marketing Intelligence Platform",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
