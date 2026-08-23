"""Local classroom REST API for DSS150P.

Run from the repository root:
    python src/local_api_server.py

Endpoint:
    http://localhost:8000/api/orders

It returns the first 100 records from data/orders.json.
No authentication is required.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "orders.json"
HOST = "127.0.0.1"
PORT = 8000

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/orders":
            records = json.loads(DATA_FILE.read_text(encoding="utf-8"))[:100]
            payload = json.dumps({
                "count": len(records),
                "records": records
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            payload = json.dumps({
                "error": "Not found",
                "available_endpoint": "/api/orders"
            }).encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

if __name__ == "__main__":
    print(f"Serving DSS150P API at http://{HOST}:{PORT}/api/orders")
    HTTPServer((HOST, PORT), Handler).serve_forever()
