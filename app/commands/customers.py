from commands.calendar import logger
from services.db_service import DatabaseFactory
# from services import database_service
from commands.utils import is_string_non_empty


def client_details(params):
    """
    Get detailed information about the client.
    Postgres (Sundea): needs {company: "sundea", first_name: str, last_name: str}
    MySQL (OptiVendi): needs {company: "optivendi", name: str}
    """

    if not isinstance(params, dict):
        return {"error": "Invalid params: expected dict"}

    company = params.get("company")
    if not is_string_non_empty([company]):
        return {"error": "Missing or invalid company parameter"}

    try:
        db = DatabaseFactory.get_database(company)

        if company.lower() == "sundea":
            first_name = params.get("first_name")
            last_name = params.get("last_name")
            if not is_string_non_empty([first_name, last_name]):
                return {"error": "first_name and last_name must be non-empty"}
            result = db.get_client(first_name=first_name, last_name=last_name)

        elif company.lower() == "optivendi":
            name = params.get("name")
            if not is_string_non_empty([name]):
                return {"error": "name must be non-empty"}
            result = db.get_client(name=name)

        else:
            return {"error": f"Unsupported company: {company}"}

        return {"data": result}

    except Exception as e:
        logger.exception(f"Exception during fetching client data: {e}")
        return {"error": f"Exception that caused error: {str(e)}"}


def get_client_installation(params):
    """
    Get client's installation details.
    Works only for Postgres (Sundea).
    Requires {company: str, client_id: str}
    """

    if not isinstance(params, dict):
        return {"error": "Invalid params: expected dict"}

    company = params.get("company")
    client_id = params.get("client_id")

    if not is_string_non_empty([company, client_id]):
        return {"error": "company and client_id must be non-empty"}

    if company.lower() != "sundea":
        return {"error": f"Installations are not available for company: {company}"}

    try:
        db = DatabaseFactory.get_database(company)
        result = db.get_installation_details(client_id=client_id)
        return {"data": result}

    except Exception as e:
        logger.exception(f"Exception during fetching installation data: {e}")
        return {"error": str(e)}
