# Architecture

The platform follows a simple product architecture:

1. Raw ecommerce transactions are generated or ingested as CSV.
2. The backend ML pipeline cleans the data and creates analytical features.
3. RFM scoring assigns customer-level business signals.
4. KMeans clustering discovers behavioral groups from Recency, Frequency and Monetary values.
5. Processed CSV and JSON artifacts are stored under `backend/app/data/processed`.
6. FastAPI exposes the processed outputs through REST endpoints.
7. The Next.js frontend consumes those endpoints and presents a SaaS-style dashboard.

## Data Flow

```text
generate_dataset.py
  -> app/data/raw/online_retail.csv
  -> app/ml/train_model.py
  -> app/data/processed/*.csv|*.json
  -> FastAPI services
  -> Next.js dashboard
```

## Deployment Shape

- Frontend: Vercel.
- Backend: Render, Railway or Cloud Run.
- Storage for MVP: versioned CSV/JSON artifacts.
- Future storage: PostgreSQL/Supabase for persistent customer and campaign data.
