# Classroom Setup

## Public REST API option
Use:
`https://jsonplaceholder.typicode.com/posts`

Expected: 100 JSON objects with `userId`, `id`, `title`, and `body`.

## Local REST API fallback
From the repository root:

```bash
python src/local_api_server.py
```

Then students use:

`http://localhost:8000/api/orders`

This endpoint returns 100 order records with timestamps, numeric measures,
categorical values, and a nested shipping object. It uses only the Python
standard library and requires no authentication.

## PostgreSQL
Start the container:

```bash
docker compose up -d
```

Load the sample table:

```bash
docker exec -i dss150p-postgres psql -U dss150p -d dss150p < sql/seed_support_tickets.sql
```

Verify:

```bash
docker exec -it dss150p-postgres psql -U dss150p -d dss150p   -c "SELECT COUNT(*) FROM support_tickets;"
```

Expected result: 250 rows.
