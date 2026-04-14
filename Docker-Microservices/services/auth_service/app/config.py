from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_USERS_CSV = PROJECT_ROOT / "data" / "users.csv"

class Config:
    USERS_CSV_PATH = os.getenv("USERS_CSV_PATH", str(DEFAULT_USERS_CSV))
