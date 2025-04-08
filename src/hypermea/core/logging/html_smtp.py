import logging

class HTMLSMTPHandler(logging.Handler):
    def __init__(self, email_sender, recipients, subject, email_from):
        super().__init__()
        self.email_sender = email_sender
        self.recipients = recipients
        self.subject = subject
        self.email_from = email_from

    def emit(self, record):
        try:
            message = self.format(record)
            subject = f" {record.levelname} - {self.subject}"
            self.email_sender.send(self.recipients, subject, message, sender=self.email_from)
        except Exception:
            self.handleError(record)



"""
import time
import hashlib

class DelegatingSMTPHandler(logging.Handler):
    def __init__(self, email_sender, recipients, subject_prefix, email_from, cooldown_seconds=60):
        super().__init__()
        self.email_sender = email_sender
        self.recipients = recipients
        self.subject_prefix = subject_prefix
        self.email_from = email_from
        self.cooldown_seconds = cooldown_seconds

        self._last_sent_time = 0
        self._last_fingerprint = None

    def emit(self, record):
        try:
            message = self.format(record)
            subject = f"{self.subject_prefix} {record.levelname}"

            # Generate fingerprint of the content
            fingerprint = hashlib.sha256(message.encode()).hexdigest()
            now = time.time()

            if (
                fingerprint == self._last_fingerprint and
                (now - self._last_sent_time) < self.cooldown_seconds
            ):
                # Skip: Same message and cooldown hasn't expired
                return

            self.email_sender.send(self.recipients, subject, message, sender=self.email_from)
            self._last_sent_time = now
            self._last_fingerprint = fingerprint

        except Exception:
            self.handleError(record)
"""