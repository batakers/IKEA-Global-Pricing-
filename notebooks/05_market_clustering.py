from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
COUNTRY_FILE = DATA_DIR / "country_metrics.csv"
OUTPUT_FILE = DATA_DIR / "clustering_results.csv"


def perform_market_clustering(country_df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    """
    Segment IKEA markets into clusters based on pricing and affordability dimensions.
    
    Args:
        country_df: Country-level metrics DataFrame
        n_clusters: Number of market segments
        
    Returns:
        DataFrame with cluster assignments and analysis
    """
    features = country_df[["price_index", "affordability_index", "online_availability_pct", "assortment_breadth"]].copy()
    features = features.fillna(features.mean())
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(features_scaled)
    
    silhouette = silhouette_score(features_scaled, clusters)
    
    result_df = country_df[["country", "region", "price_index", "affordability_index"]].copy()
    result_df["cluster_id"] = clusters
    result_df["silhouette_score"] = silhouette
    
    # Label clusters by business meaning
    cluster_centers = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), 
                                   columns=features.columns)
    cluster_labels = {
        0: "Premium Markets" if cluster_centers.loc[0, "price_index"] > cluster_centers["price_index"].median() else "Value Markets",
        1: "Premium Markets" if cluster_centers.loc[1, "price_index"] > cluster_centers["price_index"].median() else "Value Markets",
        2: "Emerging Markets" if n_clusters > 2 else "Balanced Markets",
        3: "Niche Markets" if n_clusters > 3 else None,
    }
    
    result_df["cluster_label"] = result_df["cluster_id"].map(cluster_labels)
    
    return result_df.sort_values("cluster_id")


def main() -> None:
    if not COUNTRY_FILE.exists():
        raise FileNotFoundError(f"Missing file: {COUNTRY_FILE}")
    
    country_df = pd.read_csv(COUNTRY_FILE)
    clustering_df = perform_market_clustering(country_df, n_clusters=4)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    clustering_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Market Clustering Results:")
    print(clustering_df.groupby("cluster_label").size())
    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
