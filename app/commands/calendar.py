import logging
from datetime import datetime, timezone
from services import google_service
from commands.utils import (is_rfc3339,
                                end_after_start_date,
                                start_date_in_future,
                                is_string_non_empty)

logger = logging.getLogger(__name__)

def list_future_events(params):
    """
    List calendar events in a date range.
    :param params:  {"start_date": str, "end_date": str}
    Dates should be in RFC3339 format: YYYY-MM-DDTHH:MM:SSZ
    Start date should not be in the past. (Start date >= today)
    """

    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with start_date and end_date'}

    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if not is_string_non_empty([start_date, end_date]):
        return {'error': f'Date is required and must be a non-empty string'}
    if not is_rfc3339(start_date) or not is_rfc3339(end_date):
        return {'error': 'Dates must be in valid RFC3339 format'}
    if not start_date_in_future(start_date):
        return {'error': 'start_date cannot be in the past'}
    if end_after_start_date(start_date, end_date):
        return {'error': 'end_date cannot be before start_date'}

    try:
        events = google_service.get_many_events(start_date=start_date,
                                       end_date=end_date)
        logger.info("Calendar events fetched successfully")
        return {'data': events}
    except Exception as e:
        logger.exception(f"Exception during fetching events data from calendar: {e}")
        return {'error': str(e)}

def get_single_event(params):
    """
    Get single event details.
    :param params: {event_id: str}
    """

    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with start_date and end_date'}

    event_id = params.get('event_id')

    if not is_string_non_empty(event_id):
        return  {'error': 'event_id should be non-empty string'}

    try:
        event = google_service.get_calendar_event(event_id=event_id)
        logger.info("Calendar event details fetched successfully")
        return {'event': event}
    except Exception as e:
        logger.exception(f"Exception during fetching event details from calendar: {e}")
        return {'error': str(e)}


def create_event(params: dict):
    """
    Create a new calendar event.
    :param params: { summary: string, description: string,
    start_date: { dateTime: dateTime(in format YYYY-MM-DDTHH:MM:SSZ), timeZone: timeZone in format Europe/Warsaw},
    end_date: { dateTime: dateTime(in format YYYY-MM-DDTHH:MM:SSZ), timeZone: timeZone in format Europe/Warsaw},
    attendees: list[string], location: string - if not provided, the event will take place in "ul. Wałowa 3, 43-100 Skoczów" }
    """

    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with summary, description, start date, '
                         'end date, attendees and optional location'}

    summary = params.get('summary')
    description = params.get('description') or "Wydarzenie utworzone przez Agenta AI z telefonicznej obsługi klienta"
    start_date = params.get('start_date')
    end_date = params.get('end_date')
    attendees = params.get('attendees')
    location = params.get('location') or ""

    if not location.strip():
        location = "ul. Wałowa 3, 43-100 Skoczów"

    if not isinstance(attendees, list):
        return {'error': 'attendees should be a valid list of strings'}

    if not is_string_non_empty([summary]):
        return {'error': 'Value summary should be non-empty strings'}
    if not start_date_in_future(start_date['dateTime']):
        return {'error': 'start_date cannot be in the past'}
    if not end_after_start_date(start_date['dateTime'], end_date['dateTime']):
        return {'error': 'end_date cannot be before start_date'}
    if not is_rfc3339(start_date['dateTime']) or not is_rfc3339(end_date['dateTime']):
        return {'error': 'Dates must be in valid RFC3339 format'}


    try:
        data = google_service.create_calendar_event(params)
        logger.info("Calendar event created successfully.")
        return {"data": data}
    except Exception as e:
        logger.exception("Error while creating calendar event")
        return {"error": str(e)}