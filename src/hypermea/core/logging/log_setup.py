import logging.config
import os
import html

from werkzeug.utils import secure_filename
from hypermea.core.settings import starting_environment
from .smtp_handler import HTMLSMTPHandler
from integration.smtp import EmailSender
import settings
from .. import VERSION

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class LogSetup:
    def __init__(self, service_name):
        self.service_name = service_name
        self.logging_config = self._set_base_logging_config()
        self._setup_file_logging()
        self._setup_smtp_logging()
        self._prepare_logger()

    def _prepare_logger(self):
        logging.config.dictConfig(self.logging_config)
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        logging.getLogger('pymongo').setLevel(logging.ERROR)

    def _setup_file_logging(self):
        if settings.logging.log_to_folder:
            log_folder = settings.logging.folder_to_log_to or f'/var/log/{secure_filename(self.service_name)}'
            os.makedirs(log_folder, exist_ok=True)

            log_handler = {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'simple',
                'when': 'midnight',
                'backupCount': 4,
            }

            self.logging_config['handlers']['all'] = {
                **log_handler,
                'level': 'DEBUG',
                'filename': os.path.join(log_folder, 'all.log')
            }
            self.logging_config['handlers']['warn'] = {
                **log_handler,
                'level': 'WARNING',
                'filename': os.path.join(log_folder, 'warn.log')
            }
            self.logging_config['handlers']['error'] = {
                **log_handler,
                'level': 'ERROR',
                'filename': os.path.join(log_folder, 'error.log')
            }

            self.logging_config['root']['handlers'] += ['all', 'warn', 'error']

    def _setup_smtp_logging(self):
        log = logging.getLogger("log_setup")

        if not settings.logging.log_to_email:
            return

        self.smtp_warnings = []

        smtp = settings.smtp
        logging_cfg = settings.logging

        missing = []

        if not smtp.host:
            missing.append("SMTP_HOST")
        if not smtp.port:
            missing.append("SMTP_PORT")
        if not logging_cfg.email_recipients:
            missing.append("HY_LOG_EMAIL_RECIPIENTS")

        if missing:
            for key in missing:
                self.smtp_warnings.append(
                    f'HY_LOG_TO_EMAIL is enabled, but {key} is missing — no error emails will be sent'
                )
            for warning in self.smtp_warnings:
                log.warning(warning)
            return

        email_from = (
                logging_cfg.email_from or smtp.sender or "no-reply@service.local"
        )
        recipients = [r.strip() for r in logging_cfg.email_recipients.split(",")]
        verbosity = logging_cfg.email_verbosity

        email_sender = EmailSender()

        self.logging_config["handlers"]["smtp"] = {
            "()": HTMLSMTPHandler,
            "email_sender": email_sender,
            "recipients": recipients,
            "subject": f"Problem encountered with {self.service_name}",
            "email_from": email_from,
            "level": verbosity,
            "formatter": "smtp",
            # "cooldown_seconds": 60,
        }

        self.logging_config["root"]["handlers"].append("smtp")

    def _set_base_logging_config(self):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'root': {
                'level': 'DEBUG',
                'handlers': ['console']
            },
            'formatters': {
                'simple': {
                    'format': '{asctime} - {name} - {levelname} - {message}',
                    'datefmt': DATE_FORMAT,
                    'style': '{'
                },
                'detail': {
                    'format': '{asctime} - {levelname} - File: {filename} - {funcName}() - Line: {lineno} - {message}',
                    'datefmt': DATE_FORMAT,
                    'style': '{'
                },
                'smtp': self._get_smtp_formater()
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'simple',
                    'stream': 'ext://sys.stdout'
                }
            }
        }

    @staticmethod
    def _get_smtp_formater():
        env_table = LogSetup._build_starting_environment_section()
        code_block_style = 'style="background: #f9f9f9; padding: 10px; border-radius: 4px; font-family: monospace;"'

        return {
            'datefmt': DATE_FORMAT,
            'style': '{',
            'format': f'''<h2>{{icon}} {{levelname}} - problem encountered</h2>
<div {code_block_style}>{{message}}</div>

<h3>Log Entry</h3>
<div {code_block_style}>{{asctime}} - {{name}} - {{levelname}} - {{message}}</div>

<h3>Code Location</h3>
<div {code_block_style}>
  <p>{{filename}}:{{lineno}} - {{funcName}}()</p>
  <p>{{pathname}}</p>
</div>

<h3>Starting Environment</h3>
{env_table}
'''
        }

    @staticmethod
    def _build_starting_environment_section():
        start_env = starting_environment()

        table_style = 'style="font-size: 13px; color: #666; margin-top: 10px;"'
        name_style = 'style="font-family: monospace; background: #f9f9f9; padding: 5px;"'
        value_style = 'style="padding: 5px;"'

        env_table = f'<h4>Component versions</h4><table {table_style}><tbody>'

        for component, version in start_env['versions'].items():
            env_table += f'<tr><td {name_style}>{component}</td><td {value_style}>{version}</td></tr>'
        env_table += '</tbody></table>'

        for group in [g for g in start_env['settings_groups'] if g['settings']]:
            env_table += f'<h4>{group["description"]}</h4><table {table_style}><tbody>'
            for setting, value in group['settings'].items():
                if setting == 'HY_LOG_EMAIL_FROM':
                    print(f'\n=======================\n\n\n{value}\n{html.escape(value)}\n\n=======================\n\n')
                escaped_value = html.escape(str(value))
                env_table += f'<tr><td {name_style}>{setting}</td><td {value_style}>{escaped_value}</td></tr>'
            env_table += '</tbody></table>'

        return env_table
