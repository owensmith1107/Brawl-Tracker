# BrawlTracker 

A personal data engineering pipeline that tracks and analyzes my Brawl Stars ranked game history.

## Architecture
```
Brawl Stars API → Poller (Python) → PostgreSQL (raw)
                                         ↓
                                    dbt (staging → intermediate → marts)
                                         ↓
                              FastAPI → Streamlit Dashboard
                                         ↑
                                    Dagster (hourly schedule)
```

## Tech Stack

- **Ingestion**: Python, Requests
- **Storage**: PostgreSQL
- **Transformation**: dbt-core, dbt-postgres
- **Orchestration**: Dagster
- **API**: FastAPI
- **Dashboard**: Streamlit, Plotly
- **CI**: GitHub Actions

## Features

- Automatically polls the Brawl Stars API hourly via Dagster
- Deduplicates battles so no game is ever double-counted
- dbt pipeline with 3-layer medallion architecture (staging → intermediate → marts)
- dbt tests for uniqueness, nullability, referential integrity, and accepted values
- Stats tracked:
  - Win rate by brawler and game type
  - Win rate by map and mode
  - Star player % by brawler
  - Teammate synergy (win rate with specific players)
- FastAPI layer with filterable endpoints
- Interactive Streamlit dashboard with Plotly charts
- GitHub Actions CI runs pytest and dbt build on every push

## Project Structure
```
BrawlTracker/
├── ingestion/          # API client and poller
├── db/                 # SQLAlchemy models
├── brawl_dbt/          # dbt project
│   └── models/
│       ├── staging/    # Clean raw tables
│       ├── intermediate/ # Joins and enrichment
│       └── marts/      # Final analytics tables
├── orchestration/      # Dagster assets and schedules
├── api/                # FastAPI app
├── dashboard.py        # Streamlit dashboard
├── tests/              # pytest suite
└── .github/workflows/  # CI pipeline
```

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies:
```bash
   pip install -r requirements.txt
```
3. Get a Brawl Stars API key at https://developer.brawlstars.com
4. Create a `.env` file:
```
   BRAWL_API_KEY=your_key
   PLAYER_TAG=#YOURTAG
   DB_URL=postgresql://postgres:password@localhost:5432/brawltracker
```
5. Create the database and tables:
```bash
   python db/models.py
```
6. Run the initial poll:
```bash
   python -m ingestion.poller
```
7. Run dbt:
```bash
   cd brawl_dbt && dbt run
```
8. Start the API:
```bash
   uvicorn api.main:app --reload
```
9. Start the dashboard:
```bash
   streamlit run dashboard.py
```
10. Start Dagster:
```bash
    dagster dev -f orchestration/definitions.py
```
