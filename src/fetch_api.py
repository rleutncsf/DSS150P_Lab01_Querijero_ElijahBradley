"""REST API starter. Students should extend validation and metadata capture."""

import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_records():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    records = fetch_records()
    print("Records returned:", len(records))
    print("Sample:", records[0] if records else None)
