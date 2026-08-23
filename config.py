"""Configuration helpers for DSS150P starter repository."""

import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "dss150p"),
    "user": os.getenv("DB_USER", "dss150p"),
    "password": os.getenv("DB_PASSWORD", "dss150p"),
}
