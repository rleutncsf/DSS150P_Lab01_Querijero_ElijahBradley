# Source Profile Interpretation

Findings below are drawn from the actual output of `src/profile_sources.py`
(saved in `data/evidence/profile_sources_output.txt`), not from assumption.

## customers.csv (250 rows, 7 columns, 17.76 KB)
1. **customer_id is not actually unique.** The file has 250 rows but only 247 distinct `customer_id` values, and the profiler separately found 2 fully duplicated rows. That means at least one `customer_id` repeats with different other fields (since only 2 rows are exact duplicates but 3 IDs are missing from the distinct count) - real evidence, not a hypothetical risk, that a naive `PRIMARY KEY` load would fail without a deduplication step first.
2. **email and city both have a small number of nulls (3 and 2 respectively)** while every other column is fully populated. Since `customer_id`, `first_name`, `last_name`, and `signup_date` never had a null in this sample, marking `email`/`city` as nullable but the rest as `NOT NULL` in the schema is directly supported by evidence rather than assumption.
3. signup_date parsed cleanly as a date for all 250 rows (earliest 2025-01-04, latest 2026-05-16, zero unparseable values), so treating it as `DATE` in the schema is safe - but it is still read as plain text (`str` dtype) by pandas until that parsing step is explicitly applied, so any code that skips `pd.to_datetime` and tries to sort or filter it directly would get lexicographic, not chronological, ordering.

## orders.json (250 rows, 9 columns, 76.11 KB)
1. **shipping is a nested object** (e.g. `{'region': 'Region VII', 'method': 'Standard'}`), not a flat column. This nesting is severe enough that it broke both `nunique()` and pandas' default `duplicated()` check with a `TypeError: unhashable type: 'dict'` until the profiling script was specifically patched to cast nested columns to strings before comparing rows. That is direct proof that any pipeline flattening this file naively needs a deliberate design decision (separate table, flattened columns, or a JSONB column), not an afterthought.
2. **total_amount, subtotal, and shipping_fee are numeric and internally consistent in range** (subtotal 214.40-11,997.73; shipping_fee 0-149; total_amount 214.40-12,096.73), and total_amount's minimum equals subtotal's minimum exactly when shipping_fee is 0, consistent with total_amount = subtotal + shipping_fee. This relationship should be written as an explicit validation rule rather than assumed to always hold.
3. **order_id is fully unique across all 250 rows** (250 distinct values, 0 duplicated rows), making it a solid primary-key candidate - unlike customers.csv's customer_id. customer_id here only has 159 distinct values across 250 orders, which is expected (repeat customers) and confirms it is a foreign key, not a key of this table.

## products.parquet (200 rows, 7 columns, 14.31 KB)
1. As a columnar binary format, products.parquet cannot be inspected with a text editor and required `pyarrow` to read at all - an acquisition/tooling risk worth documenting, since any future pipeline must guarantee the right library is available wherever this file is processed.
2. **unit_price ranges from 392.85 to 84,796.84** with zero nulls and no duplicate rows, and product_id is unique across all 200 rows - a clean, well-formed source overall. The one thing worth flagging: stock_quantity's minimum is 0, which is plausible (out-of-stock items) but should be confirmed with the source owner rather than assumed to always mean "temporarily unavailable" versus "discontinued."
