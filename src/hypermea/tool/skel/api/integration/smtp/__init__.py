import logging
from configuration import SETTINGS
from integration.smtp.email_sender import EmailSender

LOG = logging.getLogger('smtp')


SETTINGS.set_prefix_description('SMTP', 'Connection details for the email server')
SETTINGS.create('SMTP', {
    'HOST': 'not configured',
    'PORT': 25
})

SETTINGS.create('SMTP', 'FROM', is_optional=True)
SETTINGS.create('SMTP', 'USE_TLS', is_optional=True)
SETTINGS.create('SMTP', 'USERNAME', is_optional=True)
SETTINGS.create('SMTP', 'PASSWORD', is_optional=True)


def send_email(recipients: list[str], subject: str, message: str, sender: str = None):
    EmailSender().send(recipients, subject, message, sender)
