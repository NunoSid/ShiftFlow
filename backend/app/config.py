import json
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")

DEFAULT_DATABASE_URL = f"sqlite:///{DATA_DIR / 'turnexa.db'}"
DEFAULT_TEMPLATE_PATH = BASE_DIR / "template" / "Livro1.xlsx"

DATABASE_URL = os.getenv("SHIFTFLOW_DATABASE_URL") or DEFAULT_DATABASE_URL
TEMPLATE_PATH = Path(os.getenv("SHIFTFLOW_TEMPLATE_PATH") or DEFAULT_TEMPLATE_PATH)

APP_NAME = os.getenv("SHIFTFLOW_APP_NAME", "ShiftFlow")
ORG_NAME = os.getenv("SHIFTFLOW_ORG_NAME", "")
APP_LOGO_URL = os.getenv(
    "SHIFTFLOW_APP_LOGO_URL", os.getenv("SHIFTFLOW_LOGO_URL", "/static/logo.png")
)
ORG_LOGO_URL = os.getenv("SHIFTFLOW_ORG_LOGO_URL", "")
SHOW_APP_LOGO = os.getenv("SHIFTFLOW_SHOW_APP_LOGO", "true").lower() == "true"
SHOW_ORG_LOGO = os.getenv("SHIFTFLOW_SHOW_ORG_LOGO", "true").lower() == "true"
PRIMARY_COLOR = os.getenv("SHIFTFLOW_PRIMARY_COLOR", "#1b3a57")
ACCENT_COLOR = os.getenv("SHIFTFLOW_ACCENT_COLOR", "#4b89dc")
BACKGROUND_COLOR = os.getenv("SHIFTFLOW_BACKGROUND", "#f5f9ff")
JWT_SECRET = os.getenv("SHIFTFLOW_JWT_SECRET", "shiftflow-secret")
HOST = os.getenv("SHIFTFLOW_HOST", "0.0.0.0")
PORT = int(os.getenv("SHIFTFLOW_PORT", "8000"))
SEED_MODE = os.getenv("SHIFTFLOW_SEED_MODE", "default").lower()

def load_settings_override():
    settings_path = os.getenv("SHIFTFLOW_SETTINGS_PATH")
    if not settings_path:
        return {}
    path = Path(settings_path)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

SETTINGS_OVERRIDE = load_settings_override()

APP_NAME = SETTINGS_OVERRIDE.get("app_name", APP_NAME)
ORG_NAME = SETTINGS_OVERRIDE.get("org_name", ORG_NAME)
APP_LOGO_URL = SETTINGS_OVERRIDE.get("app_logo_url", APP_LOGO_URL)
ORG_LOGO_URL = SETTINGS_OVERRIDE.get("org_logo_url", ORG_LOGO_URL)
SHOW_APP_LOGO = SETTINGS_OVERRIDE.get("show_app_logo", SHOW_APP_LOGO)
SHOW_ORG_LOGO = SETTINGS_OVERRIDE.get("show_org_logo", SHOW_ORG_LOGO)
PRIMARY_COLOR = SETTINGS_OVERRIDE.get("primary_color", PRIMARY_COLOR)
ACCENT_COLOR = SETTINGS_OVERRIDE.get("accent_color", ACCENT_COLOR)
BACKGROUND_COLOR = SETTINGS_OVERRIDE.get("background", BACKGROUND_COLOR)
