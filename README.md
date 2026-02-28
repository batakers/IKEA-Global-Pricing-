# IKEA Global Pricing Strategy & Market Adaptation Analysis

A production-style Business Intelligence project that analyzes IKEA product pricing across 46 countries to evaluate global pricing strategy, market adaptation, and consumer affordability relative to GDP per capita.

**Key Features:**
- ✅ End-to-end data pipeline (cleaning → aggregation → insights)
- ✅ REST API with FastAPI & automatic Swagger docs
- ✅ Interactive Streamlit dashboard (3 pages)
- ✅ Professional PDF report generation
- ✅ Market clustering (K-means segmentation)
- ✅ Unit tests (17 tests, 100% pass rate)
- ✅ Docker containerization
- ✅ Pydantic data validation
- ✅ Structured logging

## Quick Start

### Local Development
```bash
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run pipeline
python notebooks/01_data_preparation.py
python notebooks/02_country_aggregation.py

# Launch dashboard
streamlit run dashboard/app.py

# Launch API
uvicorn api.main:app --reload

# Run tests
pytest tests/ -v
```

### Docker
```bash
docker-compose up -d
# Dashboard: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Data Sources

The project uses three CSV files located in `data/` folder:

| File | Description | Coverage |
|------|-------------|----------|
| `IKEA_product_catalog.csv` | IKEA product data with prices, ratings, categories by country | 46 countries, 366K+ rows |
| `exchange_rate.csv` | Currency conversion rates to USD | 40 currencies |
| `gdp_per_capita.csv` | GDP per capita for affordability analysis | 48 countries |

**Note on Data:**
- `IKEA_product_catalog.csv` is sourced from public IKEA data (Kaggle dataset or similar)
- `exchange_rate.csv` and `gdp_per_capita.csv` are provided with realistic values for analysis
- The pipeline merges these datasets and processes only countries with complete data
- Currently processes **41 countries** with all reference data available

**Running Your Own Data:**
You can replace the CSV files in `data/` folder with:
- Complete IKEA catalog from your source
- Real exchange rates from your currency provider
- Updated GDP data from World Bank API or similar

## Project Objectives

- Compare IKEA pricing by country in standardized currency (USD)
- Quantify market positioning using **Price Index**
- Evaluate affordability pressure using **Affordability Index**
- Analyze assortment breadth and online availability by market
- Segment markets into strategic groups

## Project Structure

```
IKEA-Global-Pricing/
│
├── data/
│   ├── IKEA_product_catalog.csv
│   ├── exchange_rate.csv
│   ├── gdp_per_capita.csv
│   ├── processed_catalog.csv
│   ├── country_metrics.csv
│   ├── clustering_results.csv
│   └── strategic_insights.txt
├── notebooks/
│   ├── 01_data_preparation.py
│   ├── 02_country_aggregation.py
│   ├── 03_visual_analysis.py
│   ├── 04_insight_generation.py
│   ├── 05_market_clustering.py
│   ├── 06_pdf_report.py
│   └── outputs/
├── src/
│   ├── schemas.py (Pydantic models)
│   ├── logger.py
│   └── __init__.py
├── api/
│   ├── main.py (FastAPI app)
│   └── __init__.py
├── tests/
│   ├── test_data_validation.py
│   └── __init__.py
├── dashboard/
│   └── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
├── DEPLOYMENT.md
├── ARCHITECTURE.md
└── .gitignore
```

## Feature Engineering (Country Level)

Pipeline generates these metrics:

- `avg_price_usd` - Average product price
- `avg_rating` - Average product rating
- `total_products` - Number of unique products
- `unique_categories` - Category diversity
- `global_avg_price` - Benchmark for comparison
- `price_index` = `avg_price_usd / global_avg_price`
- `affordability_index` = `avg_price_usd / gdp_per_capita`
- `price_standard_deviation` - Price volatility
- `online_availability_pct` - % products available online
- `assortment_breadth` - Sub-category count

## Data Pipeline

```
1. Data Preparation (01_data_preparation.py)
   → Clean prices, ratings, standardize countries
   → Convert currencies to USD
   → Merge with GDP data

2. Country Aggregation (02_country_aggregation.py)
   → Group by country
   → Calculate metrics
   → Compute price & affordability indexes

3. Analysis & Visualization (03_visual_analysis.py)
   → Generate maps, charts, benchmarks
   → Compare regions and product pricing

4. Insight Generation (04_insight_generation.py)
   → Extract 5 strategic insights
   → Generate 3 recommendations

5. Market Clustering (05_market_clustering.py)
   → K-means segmentation
   → Cluster countries into 4 groups

6. PDF Reporting (06_pdf_report.py)
   → Generate executive report
   → Embed metrics and visualizations
```

## API Endpoints

**Health & Stats**
```
GET /api/v1/health
GET /api/v1/statistics/global
GET /api/v1/statistics/by-region/{region}
```

**Countries**
```
GET /api/v1/countries
GET /api/v1/countries/{country_name}
GET /api/v1/countries/ranking/expensive
GET /api/v1/countries/ranking/affordable
GET /api/v1/countries/ranking/affordability-pressure
```

**Products**
```
GET /api/v1/products
GET /api/v1/products/{product_name}
```

**Clustering**
```
GET /api/v1/clustering
GET /api/v1/clustering/{cluster_label}
```

**Documentation**
```
GET /docs (Swagger UI)
GET /redoc (ReDoc)
```

## Dashboard Pages

### Page 1: Executive Overview
- KPI cards (countries, avg price, rating)
- Global pricing choropleth map
- Top 5 countries ranking

### Page 2: Pricing Strategy
- Price index ranking
- GDP vs price scatter with regression
- Product benchmark selector
- Pricing tables

### Page 3: Market Adaptation
- Affordability index
- Assortment breadth
- Online availability %

## Testing

17 unit tests, 100% pass rate:

```bash
pytest tests/test_data_validation.py -v --cov=src

# Test Coverage:
# - Data cleaning (numeric parsing, booleans, country names)
# - Pydantic schema validation
# - Business logic calculations
```

## Analysis Outputs

Generated outputs:

1. **Cleaned Dataset** - `processed_catalog.csv` (366K rows)
2. **Country Metrics** - `country_metrics.csv` (41 countries)
3. **Market Clusters** - `clustering_results.csv`
4. **Rankings**
   - Top 10 most expensive (Egypt, Morocco, Jordan, ...)
   - Top 10 cheapest (Malaysia, India, Thailand, ...)
   - Affordability pressure ranking
5. **Visualizations**
   - Global pricing choropleth
   - GDP vs price scatter
   - Product benchmarks
   - Regional category distribution
6. **Reports**
   - PDF executive report
   - Strategic insights & recommendations

## Professional Features

✅ **Production Ready**
- Docker & docker-compose
- Environment configuration (`.env`)
- Structured logging
- Error handling

✅ **Code Quality**
- Modular functions
- Comprehensive docstrings
- No redundant code
- Clear data flow

✅ **Data Integrity**
- Pydantic schema validation
- Business rule enforcement
- Robust null handling
- Currency standardization

✅ **Testing & QA**
- 17 passing unit tests
- Data validation tests
- Business logic verification
- Schema constraint tests

✅ **Documentation**
- README (this file)
- DEPLOYMENT.md (setup & running)
- ARCHITECTURE.md (system design)
- Inline code comments
- Swagger API docs

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Data Processing | pandas, numpy |
| Validation | pydantic |
| Analytics | scikit-learn |
| Visualization | plotly, seaborn, matplotlib |
| API | FastAPI, uvicorn |
| Dashboard | Streamlit |
| Testing | pytest |
| Reporting | reportlab |
| Deployment | Docker, docker-compose |

## Getting Started

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker setup
- Local development
- Environment variables
- API reference
- Troubleshooting

See [ARCHITECTURE.md](ARCHITECTURE.md) for:
- System design
- Component descriptions
- Data flow diagrams
- Technology stack details
- Performance metrics
- Security considerations

## Key Metrics

- **Data Coverage**: 366,501 product records across 41 countries
- **Global Avg Price**: ~$173 USD
- **Price Range**: $118-$265 USD (Malaysia to Egypt)
- **Market Segments**: 4 clusters (Premium, Value, Emerging, Niche)
- **Pipeline Time**: ~20 seconds (end-to-end)
- **Test Coverage**: 17 tests passing
- **API Response Time**: <100ms

---

**Ready for production deployment and hiring review.**
