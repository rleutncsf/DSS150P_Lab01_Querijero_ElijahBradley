# DSS150P Weeks 1–2 Starter Repository

This repository is intentionally incomplete. You should inspect and extend it,
not copy a completed pipeline.

## Included sources
- `data/customers.csv`
- `data/orders.json`
- `data/products.parquet`
- optional `products_optional_compare.csv` and `.json`
- `sql/seed_support_tickets.sql`
- public REST API configured in `src/fetch_api.py`

## Quick start
1. `python -m venv .venv`
2. Activate the virtual environment.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`.
5. `docker compose up -d`
6. Load `sql/seed_support_tickets.sql` into PostgreSQL.
7. Run the starter scripts.
8. Extend the code only as required by the laboratory activity.

The starter files intentionally stop before a complete data pipeline.

## REST API choices
- Public: `https://jsonplaceholder.typicode.com/posts`
- Local fallback: run `python src/local_api_server.py`, then call
  `http://localhost:8000/api/orders`

The local option is useful when your internet access is unreliable.
