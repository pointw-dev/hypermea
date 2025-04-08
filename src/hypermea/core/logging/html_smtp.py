import logging
from logging.handlers import SMTPHandler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from integration.smtp import EmailSender

class HTMLSMTPHandler(SMTPHandler):
    def __init__(self, recipients, subject_prefix='Log Alert:'):
        super().__init()
        self.email_sender = EmailSender()
        self.recipients = recipients
        self.subject_prefix = subject_prefix

    def emit(self, record):
        try:
            msg = self.format(record)
            subject = f'{self.subject_prefix} {record.levelname}'
            self.email_sender.send_email(self.recipients, subject, msg)
        except Exception:
            self.handleError(record)
