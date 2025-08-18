#
# from commands.calendar import logger
# from services import db_service
# from commands.utils import is_string_non_empty
#
#
# def client_details(params):
#     """
#     Get detailed information about the client based on their first and last name
#     :param params: {first_name: str, last_name: str}
#     """
#
#     if not isinstance(params, dict):
#         return {'error': 'Invalid params: expected object with first_name and last_name'}
#
#     first_name = params.get('first_name')
#     last_name = params.get('last_name')
#
#     if not is_string_non_empty([first_name, last_name]):
#         return {'error': 'first_name and/or last_name should be a valid non-empty string'}
#
#     try:
#         result = db_service.get_client_details(
#             first_name=first_name, last_name=last_name
#         )
#         return {'data': result}
#     except Exception as e:
#         logger.exception(f"Exception during fetching client data from database: {e}")
#         return {'error': str(e)}
#
#
# def get_client_installation(params):
#     """
#     Get client's installation details based on client id
#     :param params: { client_id: str }
#     """
#
#     if not isinstance(params, dict):
#         return {'error': 'Invalid params: expected object with client_id'}
#
#     client_id = params.get('client_id')
#
#     if not is_string_non_empty([client_id]):
#         return {'error': 'client_id should be a valid non-empty string'}
#
#     try:
#         result = db_service.get_installation_details(
#             client_id=client_id
#         )
#         return {'data': result}
#     except Exception as e:
#         logger.exception(f"Exception during fetching installaction data from database: {e}")
#         return {'error': str(e)}
