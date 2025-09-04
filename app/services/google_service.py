from datetime import datetime, timedelta
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import load_credentials, get_calendar_id
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)


def get_service():
    """
    Tworzy klienta Google Calendar API przy użyciu wczytanych poświadczeń.
    """
    creds: Credentials = load_credentials()  # zakładam, że zwraca już obiekt google.oauth2.credentials.Credentials
    service = build("calendar", "v3", credentials=creds)
    return service


def get_many_events(start_date: str, end_date: str, calendar: str):
    service = get_service()
    calendar_id = get_calendar_id(calendar)

    if start_date is None:
        start_date = datetime.utcnow().isoformat() + "Z"
    if end_date is None:
        end_date = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"

    logger.info(f"Getting `{calendar}` calendar events for {start_date} - {end_date}")

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_date,
        timeMax=end_date,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    logger.info(f"Fetched {len(events)} events")
    return events


def get_calendar_event(event_id: str, calendar: str):
    service = get_service()
    calendar_id = get_calendar_id(calendar)

    logger.info(f"Getting event {event_id} from calendar `{calendar}`")
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    return event


def create_calendar_event(event_data: dict):
    service = get_service()
    calendar_id = get_calendar_id(event_data["calendar"])
    del event_data["calendar"]

    if "location" not in event_data:
        event_data["location"] = "ul. Wałowa 3, 43-100 Skoczów"

    if "reminders" not in event_data:
        event_data["reminders"] = {"useDefault": False}

    logger.info(f"Creating event in `{calendar_id}`")
    created_event = service.events().insert(calendarId=calendar_id, body=event_data).execute()
    logger.info(f"Event created: {created_event.get('id')}")
    return created_event

