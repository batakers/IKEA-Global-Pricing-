from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "country_metrics.csv"
OUTPUT_FILE = DATA_DIR / "strategic_insights.txt"



def generate_insights(country_df: pd.DataFrame) -> tuple[list[str], list[str]]:
    top_expensive = country_df.nlargest(1, "avg_price_usd").iloc[0]
    cheapest = country_df.nsmallest(1, "avg_price_usd").iloc[0]
    highest_price_index = country_df.nlargest(1, "price_index").iloc[0]
    lowest_price_index = country_df.nsmallest(1, "price_index").iloc[0]
    least_affordable = country_df.nlargest(1, "affordability_index").iloc[0]
    most_affordable = country_df.nsmallest(1, "affordability_index").iloc[0]

    high_var_country = country_df.nlargest(1, "price_standard_deviation").iloc[0]
    broad_assortment_country = country_df.nlargest(1, "assortment_breadth").iloc[0]
    low_online_country = country_df.nsmallest(1, "online_availability_pct").iloc[0]

    insights = [
        (
            f"{top_expensive['country']} is the most expensive market with average price "
            f"${top_expensive['avg_price_usd']:.2f}, while {cheapest['country']} is the cheapest at "
            f"${cheapest['avg_price_usd']:.2f}."
        ),
        (
            f"Price positioning is most premium in {highest_price_index['country']} "
            f"(price index {highest_price_index['price_index']:.2f}) and most value-oriented in "
            f"{lowest_price_index['country']} (price index {lowest_price_index['price_index']:.2f})."
        ),
        (
            f"Affordability pressure is highest in {least_affordable['country']} "
            f"(index {least_affordable['affordability_index']:.4f}) and lowest in "
            f"{most_affordable['country']} (index {most_affordable['affordability_index']:.4f})."
        ),
        (
            f"{high_var_country['country']} shows the highest price dispersion "
            f"(std {high_var_country['price_standard_deviation']:.2f}), indicating mixed pricing tiers or assortment mix."
        ),
        (
            f"{broad_assortment_country['country']} has the widest assortment breadth "
            f"({int(broad_assortment_country['assortment_breadth'])} sub-categories), while digital availability is weakest in "
            f"{low_online_country['country']} ({low_online_country['online_availability_pct']:.1f}% online)."
        ),
    ]

    recommendations = [
        (
            f"Introduce market-specific entry-price SKUs in {least_affordable['country']} and similar high-pressure markets "
            "to improve affordability without eroding global brand value."
        ),
        (
            f"Review premium pricing justification in {highest_price_index['country']} using competitor benchmarks and "
            "elasticity testing to protect volume growth."
        ),
        (
            f"Prioritize e-commerce enablement in {low_online_country['country']} and low-online peers to expand reach, "
            "especially for categories with strong global demand."
        ),
    ]

    return insights, recommendations



def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing file: {INPUT_FILE}. Run 02_country_aggregation.py first.")

    country_df = pd.read_csv(INPUT_FILE)
    insights, recommendations = generate_insights(country_df)

    lines = ["IKEA Global Pricing Strategy - Strategic Insights", "", "5 Strategic Business Insights:"]
    lines.extend([f"{idx}. {text}" for idx, text in enumerate(insights, start=1)])
    lines.append("")
    lines.append("3 Strategic Recommendations:")
    lines.extend([f"{idx}. {text}" for idx, text in enumerate(recommendations, start=1)])

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print(f"\nSaved insights to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
