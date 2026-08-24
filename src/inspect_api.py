"""Retrieve and inspect a REST API response without transforming it."""
import json
from datetime import datetime, timezone
import requests

# API_URL = "https://jsonplaceholder.typicode.com/posts"
# Using the local classroom fallback server (src/local_api_server.py) because
# the public API was unreachable/blocked on this network - start the server
# first with: python src/local_api_server.py
API_URL = "http://localhost:8000/api/orders"


def main():
    response = requests.get(API_URL, timeout=20)
    print("status code:", response.status_code)
    response.raise_for_status()

    print("content-type:", response.headers.get("Content-Type"))

    payload = response.json()
    top_level_type = type(payload).__name__
    print("top-level JSON type:", top_level_type)

    if isinstance(payload, list):
        print("record count:", len(payload))
        print("sample record:", payload[0] if payload else None)
    elif isinstance(payload, dict):
        print("top-level keys:", list(payload.keys()))
        records = payload.get("records")
        if isinstance(records, list):
            print("record count:", len(records))
            print("sample record:", records[0] if records else None)
        else:
            print("no list-valued 'records' key found; structure does not "
                  "permit a simple record count without further inspection")

    out_path = "data/raw/api_snapshot.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print("saved snapshot to:", out_path)

    retrieved_at = datetime.now(timezone.utc).isoformat()
    print("retrieved_at_utc:", retrieved_at)


if __name__ == "__main__":
    main()
