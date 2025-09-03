import psycopg2


def check_connection(conn, logger):
    try:
        conn.cursor().execute("SELECT 1")
        conn.commit()
        return True
    except (psycopg2.Error, Exception) as e:
        logger.error(f"Connection check failed: {e}")
        return False