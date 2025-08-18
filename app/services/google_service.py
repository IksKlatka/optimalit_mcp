from config import load_credentials
from datetime import datetime
import requests
import json
import logging


logger = logging.getLogger(__name__)

credentials = load_credentials()

headers = {
    "Authorization": f"Bearer {credentials.token}"
}


def get_many_events(start_date: str, end_date: str) -> str:
    logger.info(f"Getting calendar events for date range: {start_date} to {end_date}")

    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    response = requests.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",

    params={
        "start_date": start_date,
        "end_date": end_date,
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
    """
    Get calendar event details based on its ID.

    """
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
    """
    Create a calendar event.
    The event_data should be a dictionary with the following keys:
    - summary: string
    - description: string
    - start: dict with keys: dateTime, timeZone - dateTime in format YYYY-MM-DDTHH:MM:SSZ, timeZone in format Europe/Warsaw
    - end: dict with keys: dateTime, timeZone - dateTime in format YYYY-MM-DDTHH:MM:SSZ, timeZone in format Europe/Warsaw
    - attendees: list of strings
    - location: string - if not provided, the event will take place in "ul. Wałowa 3, 43-100 Skoczów"
    """

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