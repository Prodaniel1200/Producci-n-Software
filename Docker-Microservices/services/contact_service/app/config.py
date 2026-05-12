from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTACT_CSV = PROJECT_ROOT / "data" / "contact_messages.csv"


class Config:
    CONTACT_CSV_PATH = os.getenv("CONTACT_CSV_PATH", str(DEFAULT_CONTACT_CSV))
