import logging
from datetime import datetime, timezone
from services import google_service
from commands.utils import (is_rfc3339, is_string_non_empty)

logger = logging.getLogger(__name__)

def list_future_events(params):
    """
    List calendar events in a date range.
    :param params:  {"start_date": str, "end_date": str}
    Dates should be in RFC3339 format: YYYY-MM-DDTHH:MM:SS+02:00
    Start date should not be in the past. (Start date >= today)
    """

    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with start_date, end_date and calendar name'}

    start_date = params.get("start_date")
    end_date = params.get("end_date")
    calendar = params.get("calendar")

    if not is_string_non_empty([start_date, end_date, calendar]):
        return {'error': f'Date and calendar name are required and must be a non-empty string'}
    try:
        datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    except ValueError:
        return {'error': 'Dates must be valid ISO8601 format'}


    try:
        events = google_service.get_many_events(start_date=start_date,
                                                end_date=end_date,
                                                calendar=calendar)
        logger.info("Calendar events fetched successfully")
        return {'data': events}
    except Exception as e:
        logger.exception(f"Exception during fetching events data from calendar: {e}")
        return {'error': str(e)}

def get_single_event(params):
    """
    Get single event details.
    :param params: {event_id: str, calendar: name}
    """

    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with event ID and calendar name'}

    event_id = params.get('event_id')
    calendar = params.get('calendar')

    if not is_string_non_empty([event_id, calendar]):
        return  {'error': 'event_id or calendar should be non-empty string'}

    try:
        event = google_service.get_calendar_event(event_id=event_id, calendar=calendar)
        logger.info("Calendar event details fetched successfully")
        return {'event': event}
    except Exception as e:
        logger.exception(f"Exception during fetching event details from calendar: {e}")
        return {'error': str(e)}


def create_event(params: dict):
    """
    Create a new calendar event.
    :param params: { calendar: str, summary: string, description: string,
    start: { dateTime: dateTime(in format YYYY-MM-DDTHH:MM:SS), timeZone: timeZone in format Europe/Warsaw},
    end: { dateTime: dateTime(in format YYYY-MM-DDTHH:MM:SS), timeZone: timeZone in format Europe/Warsaw},
    attendees: list[string], location: string - if not provided, the event will take place in "ul. Wałowa 3, 43-100 Skoczów" }
    """

    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with summary, description, start date, '
                         'end date, attendees and optional location'}

    summary = params.get('summary')
    start_date = params.get('start')
    end_date = params.get('end')
    attendees = params.get('attendees')
    location = params.get('location') or ""

    if not location.strip():
        location = "ul. Wałowa 3, 43-100 Skoczów"

    if not isinstance(attendees, list):
        return {'error': 'attendees should be a valid list of strings'}

    if not is_string_non_empty([summary]):
        return {'error': 'Value summary should be non-empty strings'}
    try:
        datetime.fromisoformat(start_date['dateTime'].replace("Z", "+00:00"))
        datetime.fromisoformat(end_date['dateTime'].replace("Z", "+00:00"))
    except ValueError:
        return {'error': 'Dates must be valid ISO8601 format'}

    try:
        data = google_service.create_calendar_event(params)
        logger.info("Calendar event created successfully.")
        return {"data": data}
    except Exception as e:
        logger.exception("Error while creating calendar event")
        return {"error": str(e)}