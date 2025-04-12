import logging
import re
import smtplib
import html2text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import settings


class EmailSender:
    def __init__(self):
        self.host = settings.smtp.host
        self.port = settings.smtp.port
        self.username = settings.smtp.username
        self.password = settings.smtp.password
        self.use_tls = settings.smtp.use_tls
        self.sender = settings.smtp.sender
        self.service_name = settings.hypermea.service_name
        self.log = logging.getLogger('email-sender')

        if self.host is None:
            raise RuntimeError("SMTP_HOST is not configured")

    def send(self, recipients: list[str], subject: str, html_message: str, sender: str = None):
        sender = sender or self.sender
        if not sender:
            raise RuntimeError("No sender provided and SMTP_FROM is not configured")

        mime_message = self._build_mime_message(recipients, sender, subject, html_message)
        self._send_mime_message(mime_message, recipients, sender)

    def _send_mime_message(self, mime_message, recipients, sender):
        try:
            with smtplib.SMTP(host=self.host, port=self.port) as smtp:
                if self.use_tls:
                    smtp.helo()
                    if smtp.has_extn("STARTTLS"):
                        smtp.starttls()

                if self.username and self.password:
                    smtp.login(self.username, self.password)

                failed = smtp.sendmail(sender, recipients, mime_message.as_string())
                self.log.debug(f'email sent to {recipients}')
                if failed:
                    self.log.error(f"Some recipients were rejected: {failed}")

        except smtplib.SMTPRecipientsRefused as e:
            self.log.error(f"All recipients were refused: {e.recipients}")
            raise
        except smtplib.SMTPHeloError as e:
            self.log.error(f"HELO error: {e}")
            raise
        except smtplib.SMTPSenderRefused as e:
            self.log.error(f"Sender address refused: {e}")
            raise
        except smtplib.SMTPDataError as e:
            self.log.error(f"SMTP data error: {e}")
            raise
        except smtplib.SMTPException as e:
            self.log.error(f"General SMTP error: {e}")
            raise
        except Exception:
            self.log.exception("Unexpected error during email send")
            raise

    def _build_mime_message(self, recipients, sender, subject, message):
        mime_message = MIMEMultipart('alternative')
        mime_message['Subject'] = subject
        mime_message['From'] = sender
        mime_message['To'] = ', '.join(recipients)

        text = self._strip_html(message)
        html = self._embed_message(message)

        mime_message.attach(MIMEText(text, 'plain'))
        mime_message.attach(MIMEText(html, 'html'))

        return mime_message

    def _embed_message(self, message):
        return f'''<html>
  <body>
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #102E2D; padding: 10px; border-radius: 8px;">
      <tbody>
      <tr>
        <td style="padding: 0; width: 1%; white-space: nowrap;">
          <img src="https://www.pointw.com/img/hypermea-service.png" alt="{self.service_name}" style="height: 40px; display: block; margin: 0;">
        </td>
        <td style="padding-left: 10px;">
          <span style="color: #CF7377; font-family: Calibri, Verdana, Tahoma, Arial, sans-serif; font-size: 20px;">
            {self.service_name}
          </span>
        </td>
      </tr>
      </tbody>
    </table>
    <div style="font-family: Calibri, Verdana, Tahoma, Arial, sans-serif; font-size:14px; margin-top:10px; margin-left:10px;">
      {message}
    </div>
  </body>
</html>'''

    def _strip_html(self, message):
        h = html2text.HTML2Text()
        h.pad_tables = True
        text = h.handle(message)
        text = re.sub(r'\s\s\s\s\n', '', text)
        return text
