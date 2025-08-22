from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from config import (SUPABASE_DB,
                        SUPABASE_HOST,
                        SUPABASE_PORT,
                        SUPABASE_USER,
                        SUPABASE_PASSWORD)
from .utils import check_connection
import logging

logger = logging.getLogger(__name__)


connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    dbname=SUPABASE_DB,
    user=SUPABASE_USER,
    password=SUPABASE_PASSWORD,
    host=SUPABASE_HOST,
    port=5432
)

conn=connection_pool.getconn()

try:
    if not check_connection(conn=conn, logger=logger):
        logger.error("Connection with Postgres failed.")
    else:
        logger.info("Connection with Postgres established successfully")
finally:
    connection_pool.putconn(conn)


def get_client_details(first_name: str,
                       last_name: str):
    """
    Get client details from client database using first_name and last_name parameter.
    """
    logger.info(f"Getting client information from the database ({first_name, last_name})")
    conn = connection_pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
            "SELECT * FROM clients WHERE first_name ILIKE %(first_name)s AND last_name ILIKE %(last_name)s",
            {'first_name': first_name, 'last_name': last_name}
            )

            records = cur.fetchall()
        return records
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        raise Exception(f"Error fetching clients: {e}")
    finally:
        logger.debug("Returning connection to pool.")
        connection_pool.putconn(conn)


def get_installation_details(client_id: int):
    """
    Fetch instalation details based on client's id.
    """
    logger.info(f"Getting client installation information from the database ({client_id})")
    conn = connection_pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM objects WHERE client_id = %(client_id)s",
                {"client_id": client_id}
            )

            records = cur.fetchall()
        logger.info("Successfully fetched installation details by client id.")
        return records
    except Exception as e:
        logger.error(f"Error fetching installation details by client id: {e}")
        raise Exception(f"Error fetching installation details by client id: {e}")
    finally:
        logger.debug("Returning connection to pool.")
        connection_pool.putconn(conn)
