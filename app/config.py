from dotenv import load_dotenv
import os
import logging


logger = logging.getLogger(__name__)

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CALENDAR_CLIENT_ID", False)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET", False)
GOOGLE_API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY", False)
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

API_KEY = os.getenv("API_KEY", False)
GOOGLE_EMAIL_PASSWORD = os.getenv("GOOGLE_EMAIL_PASSWORD", False)
GOOGLE_EMAIL_USER = os.getenv("GOOGLE_EMAIL_USER", False)
SMSAPI_TOKEN = os.getenv("SMSAPI_TOKEN", False)

SUPABASE_HOST = os.getenv("SUPABASE_HOST", "localhost")
SUPABASE_PORT = os.getenv("SUPABASE_PORT", 5432 )
SUPABASE_USER = os.getenv("SUPABASE_USER", "postgres")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD", False)
SUPABASE_DB = os.getenv("SUPABASE_DB", "postgres")

COMPANY_HEADQUARTERS=os.getenv("COMPANY_HEADQUARTERS", "Plein 2A, 3861 AJ Nijkerk, Holandia")

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def load_credentials():
    """
    Loads Google credentials from file.
    Checks both token and updates data if something is missing.
    :return: None
    """

    creds = Credentials.from_authorized_user_file(
        GOOGLE_CREDENTIALS_FILE,
        ["https://www.googleapis.com/auth/calendar"]
    )

    if creds.expired and creds.refresh_token:
        logger.info("Token expired, refreshing...")
        creds.refresh(Request())
        with open(GOOGLE_CREDENTIALS_FILE, "w") as token_file:
            token_file.write(creds.to_json())
    elif creds.expired and not creds.refresh_token:
        raise Exception("Token expired and no refresh token — you need to log in again")

    return creds