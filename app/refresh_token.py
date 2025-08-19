import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_TOKEN_FILE, SCOPES

def refresh_token():
    creds = None
    token_path = GOOGLE_TOKEN_FILE
    credentials_path = GOOGLE_CREDENTIALS_FILE

    print(f"[DEBUG] Using token path: {token_path}", file=sys.stderr)

    # jeśli token.json istnieje → wczytaj
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            print(f"[DEBUG] Failed to load existing token.json: {e}", file=sys.stderr)
            creds = None

    # jeśli brak lub nieważne → odśwież lub zaloguj
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[DEBUG] Refreshing existing token...", file=sys.stderr)
            creds.refresh(Request())
        else:
            print("[DEBUG] Starting OAuth flow...", file=sys.stderr)
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            # zabezpieczenie stdio: przenieś ewentualny output z flow na stderr
            old_stdout = sys.stdout
            sys.stdout = sys.stderr
            try:
                creds = flow.run_local_server(
                    port=8080,
                    open_browser=True,
                    access_type="offline",
                    prompt="consent"
                )
            finally:
                sys.stdout = old_stdout

        # zapis token.json
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())
            print("[DEBUG] New token.json saved", file=sys.stderr)

    return creds
