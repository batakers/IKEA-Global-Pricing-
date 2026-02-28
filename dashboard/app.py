from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="IKEA Global Pricing Strategy", layout="wide")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
COUNTRY_FILE = DATA_DIR / "country_metrics.csv"
CATALOG_FILE = DATA_DIR / "processed_catalog.csv"


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not COUNTRY_FILE.exists() or not CATALOG_FILE.exists():
        raise FileNotFoundError(
            "Missing transformed files. Run notebooks/01_data_preparation.py then notebooks/02_country_aggregation.py."
        )

    country_df = pd.read_csv(COUNTRY_FILE)
    catalog_df = pd.read_csv(CATALOG_FILE)
    return country_df, catalog_df



def price_map(country_df: pd.DataFrame):
    fig = px.choropleth(
        country_df,
        locations="country",
        locationmode="country names",
        color="avg_price_usd",
        hover_data={"price_index": ":.2f", "avg_rating": ":.2f", "affordability_index": ":.4f"},
        color_continuous_scale="Viridis",
        title="Global IKEA Average Price (USD)",
    )
    fig.update_layout(margin={"l": 0, "r": 0, "t": 50, "b": 0})
    return fig



def gdp_vs_price(country_df: pd.DataFrame):
    scatter_df = country_df.dropna(subset=["gdp_per_capita", "avg_price_usd"]).copy()
    slope, intercept = np.polyfit(scatter_df["gdp_per_capita"], scatter_df["avg_price_usd"], 1)
    x_line = np.linspace(scatter_df["gdp_per_capita"].min(), scatter_df["gdp_per_capita"].max(), 100)
    y_line = slope * x_line + intercept

    fig = px.scatter(
        scatter_df,
        x="gdp_per_capita",
        y="avg_price_usd",
        color="region",
        hover_name="country",
        title="GDP per Capita vs Average IKEA Price",
    )
    fig.add_scatter(x=x_line, y=y_line, mode="lines", name="Regression line")
    return fig



def product_benchmark(catalog_df: pd.DataFrame, selected_product: str):
    bench = (
        catalog_df[catalog_df["product_name"].str.upper() == selected_product.upper()]
        .groupby("country", as_index=False)
        .agg(avg_price_usd=("price_usd", "mean"), avg_rating=("product_rating", "mean"), listings=("product_id", "count"))
        .sort_values("avg_price_usd", ascending=False)
    )

    fig = px.bar(
        bench,
        x="country",
        y="avg_price_usd",
        hover_data=["avg_rating", "listings"],
        title=f"{selected_product} Benchmark by Country",
    )
    fig.update_layout(xaxis_tickangle=-45)
    return bench, fig



def executive_overview(country_df: pd.DataFrame) -> None:
    st.subheader("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Countries", f"{country_df['country'].nunique():,}")
    col2.metric("Global Avg Price (USD)", f"${country_df['avg_price_usd'].mean():,.2f}")
    col3.metric("Avg Product Rating", f"{country_df['avg_rating'].mean():.2f}")
    col4.metric("Avg Price Index", f"{country_df['price_index'].mean():.2f}")

    st.plotly_chart(price_map(country_df), use_container_width=True)

    st.markdown("**Top 5 Most Expensive Countries**")
    top5 = country_df.nlargest(5, "avg_price_usd")[["country", "avg_price_usd", "price_index"]]
    st.dataframe(top5, use_container_width=True)



def pricing_strategy(country_df: pd.DataFrame, catalog_df: pd.DataFrame) -> None:
    st.subheader("Pricing Strategy")

    ranking_fig = px.bar(
        country_df.sort_values("price_index", ascending=False),
        x="country",
        y="price_index",
        color="region",
        title="Price Index Ranking by Country",
    )
    ranking_fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(ranking_fig, use_container_width=True)

    st.plotly_chart(gdp_vs_price(country_df), use_container_width=True)

    product_options = sorted(catalog_df["product_name"].dropna().unique())
    default_product = "BILLY" if "BILLY" in product_options else product_options[0]
    selected_product = st.selectbox("Select product for benchmark", product_options, index=product_options.index(default_product))

    benchmark_df, benchmark_fig = product_benchmark(catalog_df, selected_product)
    st.plotly_chart(benchmark_fig, use_container_width=True)
    st.dataframe(benchmark_df.head(10), use_container_width=True)



def market_adaptation(country_df: pd.DataFrame) -> None:
    st.subheader("Market Adaptation")

    aff_fig = px.bar(
        country_df.sort_values("affordability_index", ascending=False),
        x="country",
        y="affordability_index",
        color="region",
        title="Affordability Index by Country (Avg Price / GDP per Capita)",
    )
    aff_fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(aff_fig, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        breadth_fig = px.bar(
            country_df.sort_values("assortment_breadth", ascending=False),
            x="country",
            y="assortment_breadth",
            color="region",
            title="Assortment Breadth (Unique Sub-categories)",
        )
        breadth_fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(breadth_fig, use_container_width=True)

    with col_right:
        online_fig = px.bar(
            country_df.sort_values("online_availability_pct", ascending=False),
            x="country",
            y="online_availability_pct",
            color="region",
            title="Online Availability %",
        )
        online_fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(online_fig, use_container_width=True)



def main() -> None:
    st.title("IKEA Global Pricing Strategy & Market Adaptation Analysis")

    country_df, catalog_df = load_data()

    page = st.sidebar.radio(
        "Navigate",
        ["Executive Overview", "Pricing Strategy", "Market Adaptation"],
    )

    if page == "Executive Overview":
        executive_overview(country_df)
    elif page == "Pricing Strategy":
        pricing_strategy(country_df, catalog_df)
    else:
        market_adaptation(country_df)


if __name__ == "__main__":
    main()
