import logging
from commands import  calendar, notification

logger = logging.getLogger(__name__)

COMMANDS = {
    # "get_client_info": customers.client_details,
    # "get_installations": customers.get_client_installation,
    "get_single_calendar_event": calendar.get_single_event,
    "get_calendar_events": calendar.list_future_events,
    "create_calendar_event": calendar.create_event,
    "send_sms": notification.sms_notification,
    "send_email": notification.email_notification,
}


def dispatch_tool(command: str, params: dict) -> dict:
    logger.info(f"Dispatching {command}, params={params}")
    if command not in COMMANDS:
        return {"error": f"Unknown tool: {command}"}
    try:
        return {"result": COMMANDS[command](params)}
    except Exception as e:
        logger.exception(f"Error in tool {command}")
        return {"error": str(e)}
