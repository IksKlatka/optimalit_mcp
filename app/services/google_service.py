from config import load_credentials, get_calendar_id
from datetime import datetime
import requests
import json
import logging


logger = logging.getLogger(__name__)

def get_headers():
    creds = load_credentials()
    return {
        "Authorization": f"Bearer {creds.token}"
    }


def get_many_events(start_date: str, end_date: str, calendar: str) -> str:
    headers = get_headers()
    logger.info(f"Getting `{calendar}` calendar events for date range: {start_date} to {end_date}")

    calendar_id = get_calendar_id(calendar)

    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    response = requests.get(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events",

    params={
        "timeMin": start_date,
        "timeMax": end_date,
    },
        headers=headers,
    )

    response.raise_for_status()
    if response.status_code == 200:
        logger.info(f"`{calendar}` calendar events fetched successfully: {response.json()}")
        return json.dumps(response.json())
    else:
        logger.error(f"Failed to get `{calendar}` calendar events: {response.status_code}")
        raise Exception(f"Failed to get `{calendar}` calendar events: {response.status_code}")


def get_calendar_event(event_id: str, calendar: str) -> str:
    headers = get_headers()
    logger.info(f"Getting calendar event: {event_id}")

    calendar_id = get_calendar_id(calendar)

    response = requests.get(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}",
        headers=headers,
    )

    response.raise_for_status()

    if response.status_code == 200:
        logger.info(f"`{calendar}` calendar event fetched successfully: {response.json()}")
        return json.dumps(response.json())
    else:
        logger.error(f"Failed to get `{calendar}` calendar event: {response.status_code}")
        raise Exception(f"Failed to get `{calendar}` calendar event: {response.status_code}")


def create_calendar_event(event_data: dict) -> str:
    headers = get_headers()
    logger.info(f"Creating calendar event.")

    calendar_id = get_calendar_id(event_data['calendar'])
    del event_data['calendar']

    if "location" not in event_data:
        event_data["location"] = "ul. Wałowa 3, 43-100 Skoczów"

    event_data['reminders'] = {
        "useDefault": False
    }

    response = requests.post(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events",
        json=event_data,
        headers=headers,
    )

    response.raise_for_status()
    if response.status_code == 200:
        logger.info(f"`{calendar_id}` calendar event created successfully: {response.json()}")
        return json.dumps(response.json())
    else:
        logger.error(f"Failed to create `{calendar_id}` calendar event: {response.status_code}")
        raise Exception(f"Failed to create `{calendar_id}` calendar event: {response.status_code}")