from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "notebooks" / "outputs"
COUNTRY_FILE = DATA_DIR / "country_metrics.csv"
CATALOG_FILE = DATA_DIR / "processed_catalog.csv"



def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not COUNTRY_FILE.exists() or not CATALOG_FILE.exists():
        raise FileNotFoundError(
            "Missing input files. Run 01_data_preparation.py and 02_country_aggregation.py first."
        )

    country_metrics = pd.read_csv(COUNTRY_FILE)
    clean_catalog = pd.read_csv(CATALOG_FILE)
    return country_metrics, clean_catalog



def top_10_expensive_cheapest(country_metrics: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    top_expensive = country_metrics.nlargest(10, "avg_price_usd")[["country", "avg_price_usd", "price_index"]]
    top_cheapest = country_metrics.nsmallest(10, "avg_price_usd")[["country", "avg_price_usd", "price_index"]]
    return top_expensive, top_cheapest



def create_global_price_map(country_metrics: pd.DataFrame):
    fig = px.choropleth(
        country_metrics,
        locations="country",
        locationmode="country names",
        color="avg_price_usd",
        hover_data={
            "price_index": ":.2f",
            "affordability_index": ":.4f",
            "avg_rating": ":.2f",
        },
        color_continuous_scale="Viridis",
        title="Global IKEA Average Price (USD)",
    )
    fig.update_layout(margin={"l": 0, "r": 0, "t": 50, "b": 0})
    return fig



def create_gdp_vs_price_scatter(country_metrics: pd.DataFrame):
    scatter_df = country_metrics.dropna(subset=["gdp_per_capita", "avg_price_usd"]).copy()
    slope, intercept = np.polyfit(scatter_df["gdp_per_capita"], scatter_df["avg_price_usd"], 1)
    x_line = np.linspace(scatter_df["gdp_per_capita"].min(), scatter_df["gdp_per_capita"].max(), 100)
    y_line = slope * x_line + intercept

    fig = px.scatter(
        scatter_df,
        x="gdp_per_capita",
        y="avg_price_usd",
        color="region",
        hover_name="country",
        title="GDP per Capita vs IKEA Average Price",
    )
    fig.add_scatter(x=x_line, y=y_line, mode="lines", name="Regression line")
    return fig



def create_product_benchmark(clean_catalog: pd.DataFrame, product_name: str = "BILLY"):
    benchmark_df = (
        clean_catalog[clean_catalog["product_name"].str.upper() == product_name.upper()]
        .groupby("country", as_index=False)
        .agg(avg_price_usd=("price_usd", "mean"), avg_rating=("product_rating", "mean"), listings=("product_id", "count"))
        .sort_values("avg_price_usd", ascending=False)
    )

    fig = px.bar(
        benchmark_df,
        x="country",
        y="avg_price_usd",
        hover_data=["avg_rating", "listings"],
        title=f"{product_name} Price Benchmark by Country",
    )
    fig.update_layout(xaxis_tickangle=-45)
    return benchmark_df, fig



def create_category_distribution_by_region(clean_catalog: pd.DataFrame) -> None:
    region_map = (
        pd.read_csv(COUNTRY_FILE)[["country", "region"]]
        .drop_duplicates()
    )
    merged = clean_catalog.merge(region_map, on="country", how="left")

    category_distribution = (
        merged.groupby(["region", "main_category"], as_index=False)
        .size()
        .rename(columns={"size": "product_count"})
    )

    plt.figure(figsize=(14, 7))
    sns.barplot(
        data=category_distribution,
        x="region",
        y="product_count",
        hue="main_category",
        estimator=sum,
        errorbar=None,
    )
    plt.title("Category Distribution Comparison by Region")
    plt.xlabel("Region")
    plt.ylabel("Product Count")
    plt.xticks(rotation=30)
    plt.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / "category_distribution_by_region.png", dpi=200)
    plt.close()



def main() -> None:
    country_metrics, clean_catalog = load_data()

    expensive_df, cheapest_df = top_10_expensive_cheapest(country_metrics)
    print("\nTop 10 Most Expensive Countries")
    print(expensive_df.to_string(index=False))

    print("\nTop 10 Cheapest Countries")
    print(cheapest_df.to_string(index=False))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    world_map = create_global_price_map(country_metrics)
    world_map.write_html(OUTPUT_DIR / "global_pricing_map.html")

    gdp_scatter = create_gdp_vs_price_scatter(country_metrics)
    gdp_scatter.write_html(OUTPUT_DIR / "gdp_vs_price_scatter.html")

    benchmark_df, benchmark_fig = create_product_benchmark(clean_catalog, product_name="BILLY")
    benchmark_fig.write_html(OUTPUT_DIR / "billy_benchmark.html")
    benchmark_df.to_csv(OUTPUT_DIR / "billy_benchmark_table.csv", index=False)

    create_category_distribution_by_region(clean_catalog)

    print(f"\nVisualization assets saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
