"""Model evaluation helper for the trained clustering pipeline."""
import json
import os


PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
METRICS_PATH = os.path.join(PROCESSED_DIR, "model_metrics.json")


def load_metrics(path: str = METRICS_PATH) -> dict:
    with open(path) as f:
        return json.load(f)


def print_model_report(metrics: dict) -> None:
    print("AI Marketing Intelligence Platform - Model Report")
    print("=" * 56)
    print(f"Clusters: {metrics['n_clusters']}")
    print(f"Silhouette score: {metrics['silhouette_score']}")
    print(f"Inertia: {metrics['inertia']}")
    print()
    print("K evaluation:")
    for k, silhouette, inertia in zip(
        metrics.get("eval_k", []),
        metrics.get("eval_silhouette", []),
        metrics.get("eval_inertia", []),
    ):
        print(f"  k={k}: silhouette={silhouette:.4f}, inertia={inertia:.2f}")


if __name__ == "__main__":
    print_model_report(load_metrics())
