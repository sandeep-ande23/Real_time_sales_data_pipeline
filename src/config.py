import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "sales_pipeline"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
}

INCOMING = ROOT / "data" / "incoming"
PROCESSED = ROOT / "data" / "processed"
FAILED = ROOT / "data" / "failed"
LOG_DIR = ROOT / "logs"

for path in (INCOMING, PROCESSED, FAILED, LOG_DIR):
    path.mkdir(parents=True, exist_ok=True)
