"""Starter source-inspection code. Extend this during the laboratory."""

from pathlib import Path
import csv
import json

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def inspect_csv(path: Path) -> None:
    # TODO: count rows, profile nulls, inspect duplicates and infer data types.
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        first_row = next(reader)
    print("CSV columns:", list(first_row.keys()))

def inspect_json(path: Path) -> None:
    # TODO: inspect keys, nested fields, date/time fields and numeric fields.
    records = json.loads(path.read_text(encoding="utf-8"))
    print("JSON record count:", len(records))
    print("First record keys:", list(records[0].keys()))

if __name__ == "__main__":
    inspect_csv(DATA_DIR / "customers.csv")
    inspect_json(DATA_DIR / "orders.json")
