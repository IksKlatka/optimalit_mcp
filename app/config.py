from dotenv import load_dotenv
import os
import json
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


logger = logging.getLogger(__name__)
load_dotenv()

API_ACCESS_TOKEN = os.getenv('API_ACCESS_TOKEN', False)
GOOGLE_CLIENT_ID = (
    os.getenv("GOOGLE_CALENDAR_CLIENT_ID")
    or os.getenv("GOOGLE_CLIENT_ID")
    or False
)
GOOGLE_CLIENT_SECRET = (
    os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET")
    or os.getenv("GOOGLE_CLIENT_SECRET")
    or False
)
GOOGLE_API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY", False)

DEFAULT_CREDS_FILE = os.path.join(os.path.dirname(__file__), "google_credentials.json")
DEFAULT_TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")

GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", DEFAULT_CREDS_FILE)
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", DEFAULT_TOKEN_FILE)

SERVICE_CALENDAR = os.getenv("SERVICE_CALENDAR")
FORMALITIES_CALENDAR = os.getenv("FORMALITIES_CALENDAR")
PRODUCT_MEETING_CALENDAR = os.getenv("CLIENT_MEETING_CALENDAR")

API_KEY = os.getenv("API_KEY", False)
GOOGLE_EMAIL_PASSWORD = os.getenv("GOOGLE_EMAIL_PASSWORD", False)
GOOGLE_EMAIL_USER = os.getenv("GOOGLE_EMAIL_USER", False)
SMSAPI_TOKEN = os.getenv("SMSAPI_TOKEN", False)

SUPABASE_HOST = os.getenv("SUPABASE_HOST", "localhost")
SUPABASE_PORT = int(os.getenv("SUPABASE_PORT", 5432))
SUPABASE_USER = os.getenv("SUPABASE_USER", "postgres")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD", False)
SUPABASE_DB = os.getenv("SUPABASE_DB", "postgres")

COMPANY_HEADQUARTERS = os.getenv("COMPANY_HEADQUARTERS", "Plein 2A, 3861 AJ Nijkerk, Holandia")


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def check_access_token(token: str):
    if token != API_ACCESS_TOKEN:
        logger.error("Wrong access token, access denied")
        return False

def get_calendar_id(calendar: str) -> str:
    calendars = {
        "service_calendar": SERVICE_CALENDAR,
        "formalities_calendar": FORMALITIES_CALENDAR,
        "product_meeting_calendar":  PRODUCT_MEETING_CALENDAR
    }

    return calendars[calendar.lower()]

def ensure_proper_token_format(path=GOOGLE_TOKEN_FILE):
    with open(path, "r") as f:
        data = json.load(f)

    if data.get("type") == "authorized_user" and "refresh_token" in data:
        return path

    converted = {
        "client_id": data.get("client_id"),
        "client_secret": data.get("client_secret"),
        "refresh_token": data.get("refresh_token"),
        "type": "authorized_user"
    }

    missing = [k for k, v in converted.items() if not v]
    if missing:
        raise ValueError(f"Brakuje pól {missing} w {path} — zaloguj się ponownie.")

    with open(path, "w") as f:
        json.dump(converted, f, indent=2)

    return path


def load_credentials(token_path=GOOGLE_TOKEN_FILE):
    if not os.path.exists(token_path):
        raise FileNotFoundError(f"token.json file on path {token_path} not found, log in to create the file")

    token_path = ensure_proper_token_format(token_path)

    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if creds.expired and creds.refresh_token:
        logger.info("Token expired, refreshing...")
        creds.refresh(Request())
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())
    elif creds.expired and not creds.refresh_token:
        raise Exception("Token expired and no refresh token — you have authorize again.")

    return creds

