import logging
from mcp.server import FastMCP
from dispatcher import dispatch_tool
from services.db_service import connection_pool
from services.utils import check_connection
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="my_mcp_server",
    version="0.1.0",
    description="MCP server exposing database, calendar and notifications",
    host="0.0.0.0",
    port=8000,
)


def check_db_connection():
    """Sprawdzenie czy baza działa na starcie serwera"""
    conn = connection_pool.getconn()
    try:
        if not check_connection(conn=conn, logger=logger):
            logger.error("Connection with Postgres failed.")
        else:
            logger.info("Connection with Postgres established successfully")
    finally:
        connection_pool.putconn(conn)


@mcp.tool(name="execute")
def execute_command(command: str, params: dict) -> dict:
    """
    Generic tool: dispatchuje komendy z katalogu commands/
    """
    logger.info(f"execute called -> {command}({params})")
    return dispatch_tool(command, params)


if __name__ == "__main__":
    logger.info(f"Starting MCP SSE server on {mcp.settings.host}:{mcp.settings.port}")
    check_db_connection()
    mcp.run(transport="stdio")
