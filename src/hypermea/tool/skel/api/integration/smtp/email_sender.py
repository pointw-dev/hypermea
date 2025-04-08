import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configuration import SETTINGS


class EmailSender:
    def __init__(self):
        self.host = SETTINGS.get("SMTP_HOST", "not configured")
        self.port = SETTINGS.get("SMTP_PORT", 25)
        self.username = SETTINGS.get("SMTP_USERNAME")
        self.password = SETTINGS.get("SMTP_PASSWORD")
        self.use_tls = SETTINGS.has_enabled("SMTP_USE_TLS")
        self.sender = SETTINGS.get("SMTP_FROM")
        self.api_name = SETTINGS.get("HY_API_NAME", "hypermea-service")
        self.log = logging.getLogger('email-sender')


        if self.host == "not configured":
            raise RuntimeError("SMTP_HOST is not configured")

    def send(self, recipients: list[str], subject: str, message: str, sender: str = None):
        sender = sender or self.sender
        if not sender:
            raise RuntimeError("No sender provided and SMTP_FROM is not configured")

        mime_message = self._build_mime_message(recipients, sender, subject, message)
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
        html = self._convert_to_html(message)

        mime_message.attach(MIMEText(text, 'plain'))
        mime_message.attach(MIMEText(html, 'html'))

        return mime_message

    def _convert_to_html(self, message):
        body = message.replace('\n', '<br/>')
        return f'''<html>
  <body>
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #102E2D; padding: 10px; border-radius: 8px;">
      <tr>
        <td style="padding: 0; width: 1%; white-space: nowrap;">
          <img src="https://www.pointw.com/img/hypermea-api.png" alt="{self.api_name}" style="height: 40px; display: block; margin: 0;">
        </td>
        <td style="padding-left: 10px;">
          <span style="color: #CF7377; font-family: Calibri, Verdana, Tahoma, Arial, sans-serif; font-size: 20px;">
            {self.api_name}
          </span>
        </td>
      </tr>
    </table>
    <div style="font-family: Calibri, Verdana, Tahoma, Arial, sans-serif; font-size:14px; margin-top:10px; margin-left:10px;">
      {body}
    </div>
  </body>
</html>'''

    def _strip_html(self, message):
        return re.sub(r'<.*?>', '', message)
