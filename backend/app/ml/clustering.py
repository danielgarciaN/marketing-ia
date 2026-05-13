"""
Clustering: KMeans + PCA for customer segmentation.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import joblib
import os

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts")


def prepare_features(rfm: pd.DataFrame) -> tuple:
    """Scale RFM features for clustering."""
    features = ["Recency", "Frequency", "Monetary"]
    X = rfm[features].copy()

    # Log-transform skewed features
    X["Monetary"] = np.log1p(X["Monetary"])
    X["Frequency"] = np.log1p(X["Frequency"])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler, features


def find_optimal_k(X_scaled: np.ndarray, k_range: range = range(2, 11)) -> dict:
    """Evaluate different k values using elbow and silhouette methods."""
    results = {"k": [], "inertia": [], "silhouette": []}

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
        labels = km.fit_predict(X_scaled)
        results["k"].append(k)
        results["inertia"].append(km.inertia_)
        results["silhouette"].append(silhouette_score(X_scaled, labels))

    return results


def train_kmeans(X_scaled: np.ndarray, n_clusters: int = 5) -> KMeans:
    """Train final KMeans model."""
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
    model.fit(X_scaled)
    return model


def apply_pca(X_scaled: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Reduce dimensions for visualization."""
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    return X_pca, pca


def interpret_clusters(rfm: pd.DataFrame) -> dict:
    """Generate cluster interpretations based on statistics."""
    interpretations = {}
    cluster_stats = rfm.groupby("Cluster").agg(
        count=("CustomerID", "count"),
        avg_recency=("Recency", "mean"),
        avg_frequency=("Frequency", "mean"),
        avg_monetary=("Monetary", "mean"),
        avg_order_value=("AvgOrderValue", "mean"),
    ).round(2)

    global_avg_r = rfm["Recency"].mean()
    global_avg_f = rfm["Frequency"].mean()
    global_avg_m = rfm["Monetary"].mean()

    for cluster_id, row in cluster_stats.iterrows():
        traits = []
        if row["avg_recency"] < global_avg_r * 0.5:
            traits.append("very recent buyers")
        elif row["avg_recency"] < global_avg_r:
            traits.append("recent buyers")
        else:
            traits.append("inactive or lapsed")

        if row["avg_frequency"] > global_avg_f * 2:
            traits.append("very high frequency")
        elif row["avg_frequency"] > global_avg_f:
            traits.append("above-average frequency")
        else:
            traits.append("low frequency")

        if row["avg_monetary"] > global_avg_m * 2:
            traits.append("high spenders")
        elif row["avg_monetary"] > global_avg_m:
            traits.append("moderate spenders")
        else:
            traits.append("low spenders")

        interpretations[int(cluster_id)] = {
            "size": int(row["count"]),
            "avg_recency": float(row["avg_recency"]),
            "avg_frequency": float(row["avg_frequency"]),
            "avg_monetary": float(row["avg_monetary"]),
            "avg_order_value": float(row["avg_order_value"]),
            "traits": traits,
            "description": f"Cluster {cluster_id}: {', '.join(traits)} ({int(row['count'])} customers)",
        }

    return interpretations


def save_artifacts(scaler, model, pca=None):
    """Save trained artifacts."""
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    joblib.dump(scaler, os.path.join(ARTIFACTS_DIR, "scaler.joblib"))
    joblib.dump(model, os.path.join(ARTIFACTS_DIR, "kmeans_model.joblib"))
    if pca is not None:
        joblib.dump(pca, os.path.join(ARTIFACTS_DIR, "pca.joblib"))
    print(f"Artifacts saved to {ARTIFACTS_DIR}")


def run_clustering_pipeline(rfm: pd.DataFrame, n_clusters: int = 5) -> tuple:
    """Full clustering pipeline."""
    X_scaled, scaler, features = prepare_features(rfm)

    # Find optimal k
    eval_results = find_optimal_k(X_scaled)
    best_k_idx = np.argmax(eval_results["silhouette"])
    suggested_k = eval_results["k"][best_k_idx]
    print(f"Best k by silhouette: {suggested_k} (score={eval_results['silhouette'][best_k_idx]:.3f})")

    # Use provided or suggested k
    k = n_clusters or suggested_k
    model = train_kmeans(X_scaled, k)
    rfm["Cluster"] = model.labels_

    # PCA
    X_pca, pca = apply_pca(X_scaled)
    rfm["PCA_1"] = X_pca[:, 0]
    rfm["PCA_2"] = X_pca[:, 1]

    # Interpret
    interpretations = interpret_clusters(rfm)

    # Metrics
    sil_score = silhouette_score(X_scaled, model.labels_)
    metrics = {
        "n_clusters": k,
        "silhouette_score": round(sil_score, 4),
        "inertia": round(model.inertia_, 2),
        "eval_results": eval_results,
    }

    # Save
    save_artifacts(scaler, model, pca)

    return rfm, interpretations, metrics
