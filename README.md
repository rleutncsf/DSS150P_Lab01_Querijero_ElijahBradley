# DSS150P Lab 01 - Elijah Bradley Querijero

## Purpose
Set up a reproducible local data-engineering environment and perform a
first-pass technical assessment of five source types (CSV, JSON, Parquet,
REST API, PostgreSQL) prior to building any production pipeline.

## Software Requirements
- Python 3.x
- Git
- Docker Desktop / Docker Engine + Compose
- A code editor (VS Code recommended)

## Reproducing the Environment (Windows / PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
docker compose up -d
Get-Content sql\seed_support_tickets.sql | docker exec -i dss150p-postgres psql -U dss150p -d dss150p
docker exec -i dss150p-postgres psql -U dss150p -d dss150p < sql\01_create_schema.sql
```
(Use `Get-Content sql\01_create_schema.sql | docker exec -i dss150p-postgres psql -U dss150p -d dss150p` instead of the `<` form above, since PowerShell does not support bash-style input redirection.)

## Reproducing the Environment (macOS / Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
docker exec -i dss150p-postgres psql -U dss150p -d dss150p < sql/seed_support_tickets.sql
docker exec -i dss150p-postgres psql -U dss150p -d dss150p < sql/01_create_schema.sql
```

## Starting/Stopping PostgreSQL
- Start: `docker compose up -d`
- Stop (keeps data): `docker compose down`
- Stop and wipe data: `docker compose down -v`

## Running the Scripts
- `python src/verify_environment.py` - confirms database connectivity
- `python src/profile_sources.py` - profiles the CSV, JSON, and Parquet sources
- `python src/inspect_api.py` - retrieves and inspects the REST API, saves `data/raw/api_snapshot.json`

## Source Descriptions
- **customers.csv** - flat customer export; candidate primary key `customer_id`.
- **orders.json** - order records with a nested `shipping` object; requires a flattening decision before relational loading.
- **products.parquet** - columnar product catalog export; requires `pyarrow` to read.
- **REST API** - `https://jsonplaceholder.typicode.com/posts` (public placeholder), with `src/local_api_server.py` available as an offline fallback.
- **PostgreSQL `support_tickets`** - seeded relational source defined in `sql/seed_support_tickets.sql`.

## Known Limitations / Unresolved Questions
- Source ownership for all file-based sources is unconfirmed.
- `customer_segment`'s allowed values are inferred from a sample and not confirmed exhaustive.
- The REST API used is a public placeholder, not the eventual production API.
- Database credentials in `docker-compose.yml`/`.env` are local development values only (`dss150p` / `dss150p`) and are not suitable for any non-lab environment.
