from services import notification_service
import logging
import re


logger = logging.getLogger(__name__)


def sms_notification(params):
    """
    Send SMS via SMSAPI to given phone number with given content
    :param params: { phone_number: str | int, message: str }
    """

    # Basic shape validation
    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with phone_number and message'}

    phone_number = params.get('phone_number')
    message = params.get('message')

    # Normalize phone to string
    if phone_number is None:
        return {'error': 'phone_number is required'}
    phone_number = str(phone_number).strip()

    # E.164-like validation
    if not re.fullmatch(r"^[1-9]\d{7,14}$", phone_number):
        return {'error': 'phone_number must be a valid international number, e.g. +48123123123'}

    if not isinstance(message, str) or not message.strip():
        return {'error': 'message is required and must be a non-empty string'}
    if len(message) > 1000:
        return {'error': 'message is too long (max 1000 characters)'}

    try:
        result = notification_service.send_sms_notification(
            phone_number=phone_number,
            message=message
        )
        logger.info(f"SMS notification sent successfully to {phone_number}")
        return {'data': result if result is not None else 'SMS sent'}
    except Exception as e:
        logger.exception(f"Exception during sending SMS: {e}")
        return {'error': str(e)}


def email_notification(params):
    """
    Send e-mail via SMTP server and Gmail account with neccessary content.
    :param params: { email: str | list[str], subject: str, message: str }
    """

    if not isinstance(params, dict):
        return {'error': 'Invalid params: expected object with email, subject and message'}

    email_value = params.get("email")
    subject = params.get("subject")
    message = params.get("message")

    # Normalize recipients to list[str]
    if email_value is None:
        return {'error': 'email is required'}
    if isinstance(email_value, str):
        recipients = [email_value.strip()]
    elif isinstance(email_value, list):
        recipients = [str(e).strip() for e in email_value]
    else:
        return {'error': 'email must be a string or a list of strings'}

    # Validate recipients
    if not recipients:
        return {'error': 'email must not be empty'}
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    for e in recipients:
        if not re.fullmatch(email_regex, e):
            return {'error': f'Invalid email address: {e}'}

    # Validate subject and message
    if not isinstance(subject, str) or not subject.strip():
        return {'error': 'subject is required and must be a non-empty string'}
    if not isinstance(message, str) or not message.strip():
        return {'error': 'message is required and must be a non-empty string'}

    try:
        result = notification_service.send_email_notification(
            email=recipients, subject=subject, message=message
        )
        logger.info(f"E-mail notification sent successfully to {', '.join(recipients)}")
        return {'data': result if result is not None else 'Email sent'}
    except Exception as e:
        logger.exception(f"Exception during sending e-mail: {e}")
        return {'error': str(e)}