# Notebooks

The production logic for this project lives in `backend/app/ml`.

Suggested notebook structure for portfolio exploration:

- `01_eda.ipynb`: revenue, countries, products, customers and order distribution.
- `02_rfm_analysis.ipynb`: RFM metrics, quantiles and business segments.
- `03_clustering.ipynb`: KMeans evaluation, silhouette score, elbow chart and PCA.
- `04_campaign_simulation.ipynb`: scenario analysis for campaign assumptions.

Keeping the reusable code in Python modules makes the API and notebooks consistent.
