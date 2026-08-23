# Dataset Guide

## customers.csv
250 rows. Identifier: `customer_id`. Includes contact/location fields, a signup date,
and customer segment. A small number of missing and duplicate values are deliberate.

## orders.json
250 records. Includes `order_timestamp`, numeric measures such as `total_amount`,
and a nested `shipping` object.

## products.parquet
200 rows. Includes identifiers, categorical fields (`category`, `brand`) and numeric
fields (`unit_price`, `stock_quantity`, `weight_kg`).

Optional CSV and JSON mirrors contain the same 200 product rows, allowing a fair
format-size and read-performance comparison.

## PostgreSQL table: support_tickets
250 rows. `ticket_id` is the primary key. `assigned_agent` and `resolved_at` can be
NULL. `opened_at` and `resolved_at` are timestamps.

## REST API
The starter script uses JSONPlaceholder `/posts`, a public fake REST API suitable
for testing and classroom exercises.
