from config import load_credentials
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


def get_many_events(start_date: str, end_date: str) -> str:
    headers = get_headers()
    logger.info(f"Getting calendar events for date range: {start_date} to {end_date}")

    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    response = requests.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",

    params={
        "timeMin": start_date,
        "timeMax": end_date,
    },
        headers=headers,
    )

    response.raise_for_status()
    if response.status_code == 200:
        logger.info(f"Calendar events fetched successfully: {response.json()}")
        return json.dumps(response.json())
    else:
        logger.error(f"Failed to get calendar events: {response.status_code}")
        raise Exception(f"Failed to get calendar events: {response.status_code}")


def get_calendar_event(event_id: str) -> str:
    headers = get_headers()
    logger.info(f"Getting calendar event: {event_id}")

    response = requests.get(
        f"https://www.googleapis.com/calendar/v3/calendars/primary/events/{event_id}",
        headers=headers,
    )

    response.raise_for_status()

    if response.status_code == 200:
        logger.info(f"Calendar event fetched successfully: {response.json()}")
        return json.dumps(response.json())
    else:
        logger.error(f"Failed to get calendar event: {response.status_code}")
        raise Exception(f"Failed to get calendar event: {response.status_code}")


def create_calendar_event(event_data: dict) -> str:
    headers = get_headers()
    logger.info(f"Creating calendar event.")


    if "location" not in event_data:
        event_data["location"] = "ul. Wałowa 3, 43-100 Skoczów"

    response = requests.post(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        json=event_data,
        headers=headers,
    )

    response.raise_for_status()
    if response.status_code == 200:
        logger.info(f"Calendar event created successfully: {response.json()}")
        return json.dumps(response.json())
    else:
        logger.error(f"Failed to create calendar event: {response.status_code}")
        raise Exception(f"Failed to create calendar event: {response.status_code}")