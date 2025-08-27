import logging
from psycopg2 import pool
import psycopg2
from psycopg2.extras import RealDictCursor
from mysql import connector
from config import DATABASES

logger = logging.getLogger(__name__)


def check_connection(conn):
    try:
        conn.cursor().execute("SELECT 1")
        conn.commit()
        return True
    except (psycopg2.Error, Exception) as e:
        logger.error(f"Connection to PostgreSQL check failed: {e}")
        return False


class BaseDatabase:
    def get_client(self, *args, **kwargs):
        raise NotImplementedError

    def get_installation_details(self, *args, **kwargs):
        raise NotImplementedError


# note: Sundea database
class PostgresDatabase(BaseDatabase):
    def __init__(self, config: dict):
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=5,
            **config
        )
        conn = self.pool.getconn()
        try:
            if not check_connection(conn=conn):
                logger.error("Connection with Postgres failed.")
            else:
                logger.info("Connection with Postgres established successfully")
        finally:
            self.pool.putconn(conn)

    def get_client(self, first_name: str, last_name: str):
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT * FROM clients
                    WHERE first_name ILIKE %(first_name)s 
                    AND last_name ILIKE %(last_name)s
                    """,
                    {"first_name": first_name, "last_name": last_name},
                )
                return cur.fetchall()
        finally:
            self.pool.putconn(conn)

    def get_installation_details(self, client_id: int):
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM objects WHERE client_id = %(client_id)s",
                    {"client_id": client_id},
                )
                return cur.fetchall()
        finally:
            self.pool.putconn(conn)


# note: OptiVendi database
class MySQLDatabase(BaseDatabase):
    def __init__(self, config: dict):
        self.config = config
        try:
            conn = connector.connect(**config)
            conn.close()
            logger.info("Connection with MySQL established successfully")
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            raise

    def get_client(self, name: str):
        conn = connector.connect(**self.config)
        try:
            cur = conn.cursor(dictionary=True)
            query = """
                SELECT * FROM vending_clients
                WHERE name LIKE %s OR name LIKE %s OR name LIKE %s
            """
            params = (f"%{name.lower()}%", f"%{name}%", f"%{name.upper()}%")
            cur.execute(query, params)
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

# database dispatcher
class DatabaseFactory:
    @staticmethod
    def get_database(company: str) -> BaseDatabase:
        company = company.lower()
        if company == "sundea":
            return PostgresDatabase(DATABASES["sundea"])
        elif company == "optivendi":
            return MySQLDatabase(DATABASES["optivendi"])
        else:
            raise ValueError(f"Unknown company: {company}")
