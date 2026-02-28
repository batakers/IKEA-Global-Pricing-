from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class CountryMetricsSchema(BaseModel):
    """Validates country-level aggregated pricing metrics."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "country": "United States",
                "region": "North America",
                "avg_price_usd": 201.88,
                "avg_rating": 3.8,
                "total_products": 500,
                "unique_categories": 25,
                "global_avg_price": 176.50,
                "price_index": 1.14,
                "affordability_index": 0.0025,
                "price_standard_deviation": 150.5,
                "gdp_per_capita": 81695,
                "online_availability_pct": 92.5,
                "assortment_breadth": 120,
            }
        }
    )
    
    country: str = Field(..., min_length=1, description="Country name (standardized)")
    region: str = Field(..., description="Geographic region")
    avg_price_usd: float = Field(..., gt=0, description="Average price in USD")
    avg_rating: float = Field(..., ge=0, le=5, description="Average product rating")
    total_products: int = Field(..., gt=0, description="Total unique products")
    unique_categories: int = Field(..., gt=0, description="Count of unique categories")
    global_avg_price: float = Field(..., gt=0, description="Global benchmark price")
    price_index: float = Field(..., gt=0, description="Relative price positioning")
    affordability_index: float = Field(..., ge=0, description="Price / GDP per capita")
    price_standard_deviation: float = Field(..., ge=0, description="Price volatility")
    gdp_per_capita: Optional[float] = Field(None, gt=0, description="GDP per capita USD")
    online_availability_pct: float = Field(..., ge=0, le=100, description="% products online")
    assortment_breadth: int = Field(..., ge=0, description="Sub-category count")

    @field_validator("avg_price_usd", "global_avg_price")
    @classmethod
    def validate_price_reasonableness(cls, v):
        if v > 10000:
            raise ValueError("Price exceeds reasonable threshold ($10k)")
        return v


class ProductBenchmarkSchema(BaseModel):
    """Validates individual product pricing across countries."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "country": "United States",
                "product_name": "BILLY",
                "product_avg_price_usd": 89.99,
                "product_avg_rating": 4.5,
                "listings": 3,
            }
        }
    )
    
    country: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    product_avg_price_usd: float = Field(..., gt=0)
    product_avg_rating: float = Field(..., ge=0, le=5)
    listings: int = Field(..., gt=0)


class ClusteringResultSchema(BaseModel):
    """Validates clustering/segmentation output."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "country": "United States",
                "cluster_id": 0,
                "cluster_label": "Premium Markets",
                "silhouette_score": 0.72,
            }
        }
    )
    
    country: str = Field(..., min_length=1)
    cluster_id: int = Field(..., ge=0)
    cluster_label: str = Field(..., description="Human-friendly cluster name")
    silhouette_score: float = Field(..., ge=-1, le=1)
