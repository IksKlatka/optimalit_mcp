import logging
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from dispatcher import dispatch_tool
from logging_config import setup_logging
from refresh_token import refresh_token
from config import API_ACCESS_TOKEN
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.fastmcp import FastMCP

setup_logging()
logger = logging.getLogger(__name__)

class SimpleTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        if token == API_ACCESS_TOKEN:
            logger.info("Token verified")
            return AccessToken(
                token=token,
                client_id="my-client-id",
                scopes=["read", "write"],
                expires_at=None,
                resource="http://localhost:8000/",
            )
        logger.info("Token not verified")
        return None


mcp = FastMCP(
    name="my_mcp_server",
    version="0.1.0",
    description="MCP server exposing access to database, calendar and notifications",
    host="0.0.0.0",
    port=8000,
    token_verifier=SimpleTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("https://elevenlabs.io/app/talk-to?agent_id=agent_2301k360t7jrf13thvd4mwesv0am"),
        resource_server_url=AnyHttpUrl("http://localhost:8000/"),
    ),
)


@mcp.tool(name="get_client_details")
def get_client_details(params: dict) -> dict:
    """
    Get client details from the database.
    :param params: if { company: "sundea" then required parameters are first_name: str, last_name: str }
    :param params: if { company: "optivendi" then required parameter is name: str }
    """
    logger.info(f"get_client_details called -> ({params})")

    if not isinstance(params, dict) or "company" not in params:
        return {"error": "Missing required parameter: company"}

    return dispatch_tool("get_client_details", params)


@mcp.tool(name="get_client_installation_details")
def get_client_installation_details(params: dict) -> dict:
    """
    Get client's installation details based on client id.
    :param params: { company: "sundea", client_id: str }
    """
    logger.info(f"get_client_installation_details called -> ({params})")

    if not isinstance(params, dict) or "company" not in params:
        return {"error": "Missing required parameter: company"}

    return dispatch_tool("get_client_installation_details", params)


@mcp.tool(name="get_single_calendar_event")
def get_single_calendar_event(params: dict) -> dict:
    """
    Get calendar event details based on its ID.
    :param params: { event_id: str,
    calendar: str one of [product_meeting_calendar, service_calendar, formalities_calendar] }
    """
    logger.info(f"get_single_calendar_event called -> ({params})")
    return dispatch_tool("get_single_calendar_event", params)


@mcp.tool(name="get_calendar_events")
def get_calendar_events(params: dict) -> dict:
    """
    Get calendar events for a given date range.
    The date range should be in the RFC3339 format YYYY-MM-DDTHH:MM:SSZ.
    The start date should be before the end date
    :param params: { start_date: str, end_date: str,
    calendar: str one of [product_meeting_calendar, service_calendar, formalities_calendar]
    }
    """
    logger.info(f"get_calendar_events called -> ({params})")
    return dispatch_tool("get_calendar_events", params)


@mcp.tool(name="create_calendar_event")
def create_calendar_event(params: dict) -> dict:
    """
    Create a new calendar event.
    Summary and description can be the same.
    :param params: { calendar: str one of [product_meeting_calendar - general meetings about product and services,
    service_calendar - for installation, service and inspection of the products at client's place, \
    formalities_calendar - for subsidies and formal meetings]
    summary: string MUST include name of the client involved!,
    description: string ("wizyta serwisowa" - must include installation address!!, "spotkanie z klientem zainteresowanym (...)", "spotkanie w sprawie dofinansowania"),
    start: { dateTime: dateTime(in format YYYY-MM-DDTHH:MM:SSZ), timeZone: timeZone in format Europe/Warsaw},
    end: { dateTime: dateTime(in format YYYY-MM-DDTHH:MM:SSZ), timeZone: timeZone in format Europe/Warsaw},
    attendees: list[string], location: string - if not provided, the event will take place in "ul. Wałowa 3, 43-100 Skoczów" }
    """
    logger.info(f"create_calendar_event called -> ({params})")
    return dispatch_tool("create_calendar_event", params)


@mcp.tool(name="send_sms")
def send_sms(params: dict) -> dict:
    """
    Send SMS via SMSAPI to given phone number with given content
    :param params: { phone_number: str | int, message: str }
    """
    logger.info(f"send_sms called -> ({params})")
    return dispatch_tool("send_sms", params)


@mcp.tool(name="send_email")
def send_email(params: dict) -> dict:
    """
    Send e-mail via SMTP server and Gmail account with neccessary content.
    :param params: { email: str | list[str], subject: str, message: str }
    """

    logger.info(f"send_email called -> ({params})")
    return dispatch_tool("send_email", params)


if __name__ == "__main__":
    refresh_token()
    # logger.info(f"Starting MCP SSE server on {mcp.settings.host}:{mcp.settings.port}")
    mcp.run(transport="stdio")
