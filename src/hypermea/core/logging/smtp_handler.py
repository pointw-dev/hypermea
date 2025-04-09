import logging
from hypermea.core.utils import LEVEL_EMOJIS

class HTMLSMTPHandler(logging.Handler):
    def __init__(self, email_sender, recipients, subject, email_from):
        super().__init__()
        self.email_sender = email_sender
        self.recipients = recipients
        self.subject = subject
        self.email_from = email_from
        self.icon = ''

    def format(self, record):
        record.icon = LEVEL_EMOJIS.get(record.levelname, '')

        # Prevent base formatter from adding unformatted traceback
        if record.exc_info and self.formatter:
            tb = self.formatter.formatException(record.exc_info)
            record.exc_info = None  # prevent auto append
            record.exc_text = None
        else:
            tb = None

        if record.stack_info and self.formatter:
            si = self.formatter.formatStack(record.stack_info)
            record.stack_info = None
        else:
            si = None

        message = super().format(record)

        if tb:
            message += (
                "<h3>Traceback</h3>"
                "<pre style='color:#a00; background:#f4f4f4; padding:10px; border-radius:5px;'>"
                f"{tb}</pre>"
            )

        if si:
            message += (
                "<h3>Stack</h3>"
                "<pre style='color:#a00; background:#f4f4f4; padding:10px; border-radius:5px;'>"
                f"{si}</pre>"
            )

        return message

    def emit(self, record):
        try:
            subject = f"{LEVEL_EMOJIS.get(record.levelname, '')} {record.levelname} - {self.subject}"

            message = self.format(record)
            self.email_sender.send(self.recipients, subject, message, sender=self.email_from)
        except Exception:
            self.handleError(record)
