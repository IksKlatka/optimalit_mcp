import logging
from commands import calendar, notification, customers

logger = logging.getLogger(__name__)

COMMANDS = {
    "get_client_details": customers.client_details,
    "get_client_installation_details": customers.get_client_installation,
    "get_single_calendar_event": calendar.get_single_event,
    "get_calendar_events": calendar.list_future_events,
    "create_calendar_event": calendar.create_event,
    "send_sms": notification.sms_notification,
    "send_email": notification.email_notification,
}


def dispatch_tool(command: str, params: dict) -> dict:
    """
    Dispatch tool command to the proper handler.
    All tools expect params: dict.
    """
    logger.info(f"Dispatching command={command}, params={params}")

    if command not in COMMANDS:
        return {"error": f"Unknown tool: {command}"}

    if not isinstance(params, dict):
        return {"error": "Invalid params: must be a dict"}


    try:
        result = COMMANDS[command](params)
        return {"result": result}
    except Exception as e:
        logger.exception(f"Error while executing tool '{command}': {e}")
        return {"error": str(e)}
