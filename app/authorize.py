from app.config import GOOGLE_TOKEN_FILE, GOOGLE_CREDENTIALS_FILE
import os
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = GOOGLE_CREDENTIALS_FILE
TOKEN_FILE = GOOGLE_TOKEN_FILE

# Ustawienia logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authorize_user():
    """
    Przeprowadza OAuth2 dla użytkownika i zapisuje token.json.
    """
    creds = None

    # Jeśli token już istnieje, wczytaj go
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        logger.info("Wczytano istniejący token.json")

    # Jeśli token nie istnieje lub jest nieważny, uruchom flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Token wygasł, odświeżanie...")
            creds.refresh(Request())
        else:
            logger.info("Brak tokena lub brak refresh_token, uruchamiam logowanie użytkownika...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Stały port, żeby uniknąć redirect_uri_mismatch
            creds = flow.run_local_server(port=8080)

        # Zapisz token.json
        with open(TOKEN_FILE, "w") as token_file:
            token_file.write(creds.to_json())
            logger.info(f"Zapisano token w {TOKEN_FILE}")

    return creds


if __name__ == "__main__":
    authorize_user()
    logger.info("✅ Autoryzacja zakończona. Plik token.json gotowy do użycia.")

