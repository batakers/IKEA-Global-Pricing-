# System Architecture

## Overview

The IKEA Global Pricing project is organized as a modular data analytics platform with three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Processing Pipeline                  │
│  01_prep → 02_aggregate → 03_visualize → 04_insights        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer (CSV/Parquet)                  │
│  processed_catalog.csv, country_metrics.csv, clustering.csv  │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
        ┌─────────────────┐   ┌────────────────┐
        │  Streamlit      │   │  FastAPI       │
        │  Dashboard      │   │  REST API      │
        │  (Port 8501)    │   │  (Port 8000)   │
        └─────────────────┘   └────────────────┘
```

## Component Descriptions

### 1. Data Processing Pipeline (`notebooks/`)

**01_data_preparation.py**
- Load raw IKEA product catalog
- Clean price & rating columns (parse numeric, handle nulls)
- Standardize country names with dictionary mapping
- Convert currencies to USD using exchange rates
- Merge GDP per capita data
- Output: `processed_catalog.csv` (163K rows, 17 countries)

**02_country_aggregation.py**
- Group processed catalog by country
- Calculate country-level metrics (avg_price, rating, assortment)
- Compute price_index (country / global avg)
- Compute affordability_index (price / GDP per capita)
- Output: `country_metrics.csv` (17 rows)

**03_visual_analysis.py**
- Generate exploratory visualizations (Plotly, Seaborn, Matplotlib)
- Choropleth world map
- GDP vs price scatter with regression
- Product benchmarking charts
- Output: HTML/PNG files in `notebooks/outputs/`

**04_insight_generation.py**
- Automatic extraction of 5 strategic insights
- Generation of 3 actionable recommendations
- Output: `strategic_insights.txt`

**05_market_clustering.py**
- K-means clustering on price/affordability dimensions
- Segment markets into 4 clusters (Premium, Value, Emerging, Niche)
- Output: `clustering_results.csv`

**06_pdf_report.py**
- Generate professional PDF executive report
- Embed KPIs, tables, and insights
- Output: `IKEA_Executive_Report.pdf`

### 2. Data Validation Layer (`src/`)

**schemas.py**
- Pydantic V2 models for strict type validation
- `CountryMetricsSchema`: Validates country-level aggregates
- `ProductBenchmarkSchema`: Validates product pricing
- `ClusteringResultSchema`: Validates market segmentation
- Business rules enforcement (price bounds, rating 0-5, etc.)

**logger.py**
- Structured logging configuration
- Rotating file handler for production use
- Console + file output with different verbosity levels

### 3. REST API (`api/`)

**main.py** (FastAPI application)

**Endpoint Categories:**

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/health` | Service health check |
| `GET /api/v1/countries` | List all analyzed countries |
| `GET /api/v1/countries/{name}` | Single country metrics |
| `GET /api/v1/countries/ranking/expensive` | Top 10 expensive |
| `GET /api/v1/countries/ranking/affordable` | Top 10 affordable |
| `GET /api/v1/products/{name}` | Product pricing by country |
| `GET /api/v1/clustering` | Market segmentation results |
| `GET /api/v1/statistics/global` | Global aggregate statistics |

**Features:**
- CORS enabled for cross-origin requests
- Automatic data loading on startup
- Pydantic response validation
- Automatic OpenAPI/Swagger documentation (`/docs`)

### 4. Interactive Dashboard (`dashboard/`)

**app.py** (Streamlit application)

**Pages:**
1. **Executive Overview**
   - KPI cards (country count, global avg price, rating)
   - Global pricing choropleth map
   - Top 5 countries ranking

2. **Pricing Strategy**
   - Price index ranking bar chart
   - GDP vs price scatter with regression
   - Product benchmark selector (default: BILLY)
   - Benchmarking tables

3. **Market Adaptation**
   - Affordability index comparison
   - Assortment breadth by country
   - Online availability percentages

**Features:**
- Cached data loading (`@st.cache_data`)
- Multi-page navigation
- Interactive Plotly visualizations
- Responsive layout

### 5. Testing Suite (`tests/`)

**test_data_validation.py** (17 tests, 100% pass rate)

**Test Classes:**
- `TestDataCleaning`: Numeric parsing, boolean normalization, country mapping
- `TestCountryMetricsValidation`: Schema validation, field constraints
- `TestProductBenchmarkValidation`: Product pricing validation
- `TestBusinessLogic`: Price index & affordability calculations

**Coverage:**
- Data cleaning functions
- Pydantic schema enforcement
- Business logic calculations

## Data Flow

```
Raw Data (46 countries)
    ↓
[01] Data Preparation
    ├─ Clean prices/ratings
    ├─ Standardize countries
    ├─ Convert to USD
    └─ Merge GDP data
    ↓
processed_catalog.csv (163K rows)
    ↓
[02] Country Aggregation
    ├─ Group by country
    ├─ Calculate metrics
    ├─ Price index
    └─ Affordability index
    ↓
country_metrics.csv (17 rows)
    ├─→ [03] Visual Analysis → outputs/ (maps, charts)
    ├─→ [04] Insights → strategic_insights.txt
    ├─→ [05] Clustering → clustering_results.csv
    └─→ [06] PDF Report → IKEA_Executive_Report.pdf
    ↓
REST API (api/main.py)
    ├─→ Dashboard (dashboard/app.py)
    └─→ External integrations
```

## Deployment Architectures

### Local Development
```
Jupyter/IDE → Python scripts → CSV files → Streamlit (local)
```

### Docker Container
```
Docker Image (Python 3.11)
    ├─ Streamlit Service (8501)
    ├─ FastAPI Service (8000)
    └─ Shared /data volume
```

### Production Cloud (e.g., AWS)
```
S3 (Data) → ECS Task (Pipeline) → RDS (optional DB) 
                                    ↓
                            ALB → EC2 (Dashboard)
                                 ALB → EC2 (API)
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data Processing | pandas, numpy | ETL and aggregation |
| Validation | pydantic | Schema enforcement |
| Visualization | plotly, seaborn, matplotlib | Charts and maps |
| API | FastAPI, uvicorn | REST microservice |
| Dashboard | Streamlit | Interactive UI |
| ML/Stats | scikit-learn | Clustering analysis |
| Reporting | reportlab | PDF generation |
| Testing | pytest | Unit test framework |
| Containerization | Docker, Docker Compose | Deployment |

## Performance Characteristics

- **Data Loading**: ~2s (17 countries CSV)
- **Pipeline Execution**: ~15s (full run)
- **Dashboard Startup**: ~5s (cached data)
- **API Response**: <100ms
- **Tests**: ~0.5s (17 tests)

## Security Considerations

- Environment variables for sensitive config (`.env` not committed)
- No hardcoded API keys or credentials
- CORS configured explicitly (not `*` in production)
- Input validation via Pydantic
- Logged errors without sensitive data exposure

## Future Enhancements

1. **Database Integration**: PostgreSQL instead of CSV
2. **Caching Layer**: Redis for API performance
3. **Prediction Models**: Time-series forecasting with Prophet
4. **Real-time Updates**: Kafka streams from pricing feeds
5. **Advanced Analytics**: Price elasticity, demand forecasting
6. **Multi-language**: i18n support for dashboard
7. **Authentication**: OAuth2 for API security
