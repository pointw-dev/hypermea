import os
import re
import logging

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from configuration import SETTINGS

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


def send_email(recipients: list[str], subject: str, message: str, sender=None):
    api_name = SETTINGS.get('HY_API_NAME', 'hypermea-service')

    host, recipients, sender = _confirm_settings(recipients, sender)
    mime_message = _build_mime_message(api_name, message, recipients, sender, subject)
    _send_mime_message(host, mime_message, recipients, sender)


def _send_mime_message(host, mime_message, recipients, sender):
    with SMTP(host=host, port=SETTINGS.get('SMTP_PORT', '25')) as smtp:
        if SETTINGS.has_enabled('SMTP_USE_TLS'):
            smtp.helo()
            if smtp.has_extn('STARTTLS'):
                smtp.starttls()

        username = SETTINGS.get('SMTP_USERNAME')
        password = SETTINGS.get('SMTP_PASSWORD')
        if username and password:
            smtp.login(username, password)

        smtp.sendmail(sender, recipients, mime_message.as_string())


def _confirm_settings(recipients, sender):
    host = SETTINGS.get('SMTP_HOST', 'not configured')
    if host == 'not configured':
        LOG.error('SMTP_HOST is not configured')
        raise RuntimeError('SMTP_HOST is not configured')
    sender = SETTINGS.get('SMTP_FROM', sender)
    if not sender:
        LOG.error('SMTP_FROM is not configured and "sender" is provided')
        raise RuntimeError('no sender provided')
    recipients = ', '.join(recipients)
    return host, recipients, sender


def _build_mime_message(api_name, message, recipients, sender, subject):
    mime_message = MIMEMultipart('alternative')
    mime_message['Subject'] = subject
    mime_message['From'] = sender
    mime_message['To'] = recipients

    message_text = _strip_html(message)
    message_html = _convert_message_to_html(api_name, message)

    mime_message.attach(MIMEText(message_text, 'plain'))
    mime_message.attach(MIMEText(message_html, 'html'))

    return mime_message


def _convert_message_to_html(api_name, message):
    message_body = message.replace('\n', '<br/>')
    message_html = f'''<html>
  <body>
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #102E2D; padding: 10px; border-radius: 8px;">
      <tr>
        <td style="padding: 0; width: 1%; white-space: nowrap;">
          <img src="https://www.pointw.com/img/hypermea-api.png" alt="{api_name}" style="height: 40px; display: block; margin: 0;">
        </td>
        <td style="padding-left: 10px;">
          <span style="color: #CF7377; font-family: Calibri, Verdana, Tahoma, Arial, sans-serif; font-size: 20px;">
            {api_name}
          </span>
        </td>
      </tr>
    </table>
    <div style="font-family: Calibri, Verdana, Tahoma, Arial, sans-serif; font-size:14px; margin-top:10px; margin-left:10px;">
      {message_body}
    </div>
  </body>
</html>
'''
    return message_html


def _strip_html(message):
    p = re.compile(r'<.*?>')
    return p.sub('', message)


