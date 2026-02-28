# Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker & Docker Compose installed

### Run Everything

```bash
cd IKEA-Global-Pricing
docker-compose up -d
```

This starts:
- **Streamlit Dashboard**: http://localhost:8501
- **FastAPI Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Individual Services

```bash
# Streamlit dashboard only
docker build -t ikea-pricing .
docker run -p 8501:8501 -v $(pwd)/data:/app/data ikea-pricing streamlit run dashboard/app.py

# FastAPI only
docker run -p 8000:8000 -v $(pwd)/data:/app/data ikea-pricing uvicorn api.main:app --host 0.0.0.0 --port 8000

# Run tests
docker run -v $(pwd)/tests:/app/tests ikea-pricing pytest tests/ -v
```

## Local Development

### Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Run Pipeline
```bash
python notebooks/01_data_preparation.py
python notebooks/02_country_aggregation.py
python notebooks/05_market_clustering.py
python notebooks/06_pdf_report.py
python notebooks/03_visual_analysis.py
```

### Run Services
```bash
# Terminal 1: Dashboard
streamlit run dashboard/app.py

# Terminal 2: API
uvicorn api.main:app --reload

# Terminal 3: Tests
pytest tests/ -v --cov=src
```

## Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key variables:
- `API_HOST`, `API_PORT` - FastAPI server config
- `STREAMLIT_PORT` - Dashboard port
- `DATA_PATH` - Input data location
- `CLUSTERING_K` - Number of market clusters
- `LOG_LEVEL` - Logging verbosity

## API Endpoints Reference

### Health & Metadata
- `GET /api/v1/health` - Service status
- `GET /api/v1/statistics/global` - Global metrics

### Country Analysis
- `GET /api/v1/countries` - All countries
- `GET /api/v1/countries/{country_name}` - Single country
- `GET /api/v1/countries/ranking/expensive` - Top expensive
- `GET /api/v1/countries/ranking/affordable` - Top affordable
- `GET /api/v1/countries/ranking/affordability-pressure` - Affordability ranking

### Product Benchmarks
- `GET /api/v1/products` - All benchmarks
- `GET /api/v1/products/{product_name}` - Product across countries

### Market Clustering
- `GET /api/v1/clustering` - All clusters
- `GET /api/v1/clustering/{cluster_label}` - Countries in cluster

### Regional Analysis
- `GET /api/v1/statistics/by-region/{region}` - Regional statistics

## Testing

Run all tests with coverage:
```bash
pytest tests/ -v --cov=src --cov=notebooks --cov-report=html
```

Test categories:
- **Data Validation**: Numeric parsing, boolean normalization, country standardization
- **Schema Validation**: Pydantic models enforce business rules
- **Business Logic**: Price index, affordability calculations

## Troubleshooting

**Port already in use:**
```bash
# Change ports in docker-compose.yml or set environment
docker run -p 9501:8501 ikea-pricing streamlit run dashboard/app.py --server.port=9501
```

**Missing data files:**
Ensure `data/IKEA_product_catalog.csv`, `exchange_rate.csv`, `gdp_per_capita.csv` exist.

**API not connecting to data:**
Run pipeline scripts first to generate `processed_catalog.csv`, `country_metrics.csv`, etc.
