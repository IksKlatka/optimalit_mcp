import requests
from app.config import (SMSAPI_TOKEN,
                        GOOGLE_EMAIL_PASSWORD,
                        GOOGLE_EMAIL_USER)
import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

def send_sms_notification(phone_number: str, message: str):
    """
    Send an SMS notification to a given phone number.
    The phone_number should be a string in the format "123456789".
    The message should be a string with no special characters.
    """
    logger.info(f"Sending SMS notification to {phone_number} with message: {message}")

    response = requests.post(
        "https://api.smsapi.pl/sms.do",
        headers={
            "Authorization": f"Bearer {SMSAPI_TOKEN}",
            },
        json={
            "to": phone_number,
            "message": message
            },
        params={
            "normalize": 1
        }
    )

    response.raise_for_status()
    if response.status_code == 200:
        logger.info(f"SMS notification sent successfully to {phone_number}")
        return response.content
    else:
        logger.error(f"Failed to send SMS notification to {phone_number}")
        raise Exception(f"Failed to send SMS notification to {phone_number}")


def send_email_notification(email: str, subject: str, message: str):
    """
    Send an email notification to a given email address.
    The email should be a string in the format "testmail.cage@gmail.com".
    The subject and message should be a string.
    """
    logger.info(f"Sending email notification to {email} with subject: {subject} and message: {message}")

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = GOOGLE_EMAIL_USER
    msg['To'] = ', '.join(email)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        try:
            logger.info("Logging in to Gmail...")
            smtp_server.login(GOOGLE_EMAIL_USER, GOOGLE_EMAIL_PASSWORD)
            logger.info("Sending email...")
            smtp_server.sendmail(GOOGLE_EMAIL_USER, email, msg.as_string())
            logger.info("Email sent!")
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise Exception(f"Error sending email: {e}")
