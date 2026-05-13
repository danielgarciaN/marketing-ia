# AI Marketing Intelligence Platform

End-to-end customer intelligence platform for ecommerce marketing teams.

The project combines data cleaning, RFM analysis, customer segmentation, KMeans clustering, campaign recommendations, automatic business insights, a FastAPI backend and a Next.js dashboard. It is designed as a portfolio-ready SaaS case study, not as a notebook-only exercise.

## Business Problem

Marketing and CRM teams need to understand who their best customers are, which users are at risk of churn, what segments drive revenue and what campaigns should be launched next. This platform turns transactional ecommerce data into actionable decisions.

## Solution

The platform provides:

- Executive dashboard with KPIs and revenue trend.
- RFM customer scoring: Recency, Frequency and Monetary value.
- Business segments: VIP, Loyal, New, At-Risk, Lost, Occasional and High Potential.
- KMeans clustering with PCA coordinates for visualization.
- Campaign recommendations per segment.
- Campaign simulator with estimated revenue, conversions, ROI and uplift.
- Rules-based AI-style insights focused on retention, revenue and growth.
- REST API with Swagger documentation.
- Frontend dashboard connected to the backend API.
- Bilingual portal UI with English and Spanish mode.

## Dataset

The project uses a synthetic ecommerce dataset generated with the same schema as the Online Retail dataset:

- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

The generator creates realistic customers, transactions, returns, missing customer IDs and international markets. The raw CSV lives in:

```text
backend/app/data/raw/online_retail.csv
```

## Architecture

```text
frontend/                  Next.js SaaS dashboard
  app/
  components/
  lib/

backend/                   FastAPI + Data Science pipeline
  app/
    api/                   REST routes
    services/              Business logic
    ml/                    Preprocess, RFM, clustering, training
    data/                  Raw and processed CSV/JSON outputs
    artifacts/             Scaler, KMeans and PCA joblib files
```

## Stack

- Python, Pandas, NumPy
- Scikit-learn, KMeans, PCA, StandardScaler, Silhouette Score
- FastAPI, Pydantic, Uvicorn
- Next.js, React, TypeScript
- Recharts

## Local Setup

Use Python 3.11. The pinned Pandas/Numpy/Scikit-learn versions are not compatible with Python 3.14.

From the repository root:

```powershell
.\.venv311\Scripts\activate
```

If you need to recreate the environment:

```powershell
py -3.11 -m venv .venv311
.\.venv311\Scripts\activate
python -m pip install --upgrade pip
pip install -r .\files\backend\requirements.txt
```

## Run the Data Pipeline

```powershell
cd files\backend
..\..\.venv311\Scripts\python.exe .\generate_dataset.py
..\..\.venv311\Scripts\python.exe -m app.ml.train_model
```

This creates:

- `app/data/processed/online_retail_clean.csv`
- `app/data/processed/customers_rfm.csv`
- `app/data/processed/dashboard_summary.json`
- `app/data/processed/revenue_monthly.json`
- `app/data/processed/segment_summary.json`
- `app/data/processed/model_metrics.json`
- `app/artifacts/kmeans_model.joblib`
- `app/artifacts/scaler.joblib`
- `app/artifacts/pca.joblib`

## Run the Backend

```powershell
cd files\backend
..\..\.venv311\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## Run the Frontend

```powershell
cd files\frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## User Guide

Spanish usage guide:

```text
docs/user_guide_es.md
```

If your API uses a different URL, create `files/frontend/.env.local`:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/dashboard/summary` | Business KPIs |
| GET | `/dashboard/revenue` | Monthly revenue |
| GET | `/customers` | Paginated customer table |
| GET | `/customers/{id}` | Customer detail |
| GET | `/segments` | Segment summary |
| GET | `/segments/{name}` | Segment detail and customers |
| GET | `/campaigns/recommendations` | Campaign playbook |
| POST | `/campaigns/simulate` | Campaign ROI simulation |
| GET | `/insights` | Automatic insights |
| GET | `/model/metrics` | KMeans metrics |
| GET | `/model/clusters` | Cluster interpretation |
| GET | `/model/cluster-points` | PCA scatter points |

## Results

The current generated dataset contains around 126k transaction rows and roughly 2k customers. The pipeline produces a complete RFM table, assigns business segments and trains a 5-cluster KMeans model. The model metrics are exposed through the API and displayed in the frontend methodology section.

## Limitations

- Dataset is synthetic, although modeled after Online Retail structure.
- Insights are rules-based rather than generated with an external LLM.
- CSV files are used for the MVP instead of a database.
- Campaign simulator uses assumptions for conversion uplift and channel costs.

## Next Steps

- Add authentication and workspace-level tenant separation.
- Persist data in PostgreSQL or Supabase.
- Connect to a real ecommerce source such as Shopify.
- Add LLM-generated insight narratives with human approval.
- Deploy frontend to Vercel and backend to Render or Railway.
