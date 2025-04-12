from . import settings
from .email_sender import EmailSender

def send_email(recipients: list[str], subject: str, html_message: str, sender: str = None):
    EmailSender().send(recipients, subject, html_message, sender)
