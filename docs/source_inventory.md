# Source Inventory

## customers.csv
- Source-system type: Flat file export (likely from a CRM or customer database)
- Data format: CSV
- Structure: Structured (tabular, one row per customer)
- Expected update pattern: Batch - likely a daily or weekly export, not real-time
- Likely acquisition method: Scheduled file drop to a shared location, or SFTP pull
- Schema location/owner: Unknown - requires confirmation from the CRM/source owner
- Possible primary/business key: customer_id
- Schema-evolution risk: New values could appear in customer_segment without notice; email format is not enforced at the source
- Data-quality risk: signup_date is a plain string until explicitly parsed; nothing guarantees email uniqueness or valid formatting

## orders.json
- Source-system type: Application/order-management system export
- Data format: JSON (array of objects)
- Structure: Semi-structured - the shipping field is a nested object ({region, method}), not a flat column
- Expected update pattern: Likely batch export, possibly more frequent than customers.csv given order volume
- Likely acquisition method: API pull or scheduled file export from the order system
- Schema location/owner: Unknown - requires confirmation from the order-management system owner
- Possible primary/business key: order_id; customer_id is a foreign key back to customers.csv
- Schema-evolution risk: If shipping gains or loses nested fields, naive flattening breaks silently; total_amount appears derived from subtotal + shipping_fee, which is a business rule that could change
- Data-quality risk: order_timestamp format must be verified for consistency; status is a free-text-looking field with an unconfirmed set of valid values

## products.parquet
- Source-system type: Likely a product catalog or inventory system export
- Data format: Parquet (columnar binary)
- Structure: Structured
- Expected update pattern: Batch, likely less frequent than orders (catalog changes slower than transactions)
- Likely acquisition method: Scheduled export/ETL job writing directly to Parquet
- Schema location/owner: Unknown - requires confirmation from the catalog system owner
- Possible primary/business key: product_id (confirm exact column name after profiling)
- Schema-evolution risk: Parquet enforces a schema at write time, but that schema can still change between export runs without downstream notice
- Data-quality risk: Numeric fields (e.g., price, stock quantity) should be checked for negative or out-of-range values; confirm no nulls in required fields such as category

## REST API (local fallback server, /api/orders)
- Source-system type: Local classroom fallback server (`src/local_api_server.py`); the public `jsonplaceholder.typicode.com/posts` endpoint returned HTTP 403 on this network, so the local fallback was used instead per the lab's documented contingency
- Data format: JSON
- Structure: Structured; top-level type is a dict with keys `count` and `records`, where `records` is a list of order objects (not a bare list)
- Expected update pattern: On-demand pull; served from a static copy of orders.json, capped at the first 100 records
- Likely acquisition method: HTTP GET request to `http://localhost:8000/api/orders`
- Schema location/owner: Defined by `src/local_api_server.py`; ultimately mirrors orders.json's schema
- Possible primary/business key: order_id
- Schema-evolution risk: External APIs can change response shape without warning and without a formal contract; this fallback in particular wraps its payload in `{count, records}` rather than returning a bare list, which any consumer must handle explicitly
- Data-quality risk: Same nested `shipping` object risk as orders.json, since the fallback serves that same data unmodified
- Retrieved at (UTC): 2026-08-23T12:43:47.631539+00:00
- Response: HTTP 200, Content-Type application/json, 100 records returned

## PostgreSQL source table (support_tickets)
- Source-system type: Relational database
- Data format: SQL table
- Structure: Structured
- Expected update pattern: Static seed for this lab; in production, likely incremental inserts as new tickets are created
- Likely acquisition method: Direct SQL query / JDBC-ODBC connection in a real pipeline
- Schema location/owner: Defined explicitly in sql/seed_support_tickets.sql
- Possible primary/business key: ticket_id (confirm exact column name using \d support_tickets)
- Schema-evolution risk: Low within this lab (schema is fixed in a seed file), but production tables can have columns added/dropped via migrations without every consumer being notified
- Data-quality risk: Confirm whether foreign keys (e.g., customer_id) are nullable, and whether status/priority fields are constrained to a fixed set of values
