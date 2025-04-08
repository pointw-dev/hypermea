import logging.config
import os

from werkzeug.utils import secure_filename
from hypermea.core.settings import starting_environment
from .html_smtp import HTMLSMTPHandler
from integration.smtp import EmailSender
from configuration import SETTINGS, VERSION

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class LogConfigurator:
    def __init__(self, api_name):
        self.api_name = api_name
        self.logging_config = self._set_base_logging_config()
        self._setup_file_logging()
        self._setup_smtp_logging()
        self._prepare_logger()

    def _prepare_logger(self):
        logging.config.dictConfig(self.logging_config)
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    def _setup_file_logging(self):
        if SETTINGS.has_enabled('HY_LOG_TO_FOLDER'):
            log_folder = SETTINGS.get('FOLDER_TO_LOG_TO') or f'/var/log/{secure_filename(self.api_name)}'
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
        if not SETTINGS.has_enabled('HY_LOG_TO_EMAIL'):
            return

        self.smtp_warnings = []
        required = ['SMTP_HOST', 'SMTP_PORT', 'HY_LOG_EMAIL_RECIPIENTS']
        good_to_go = True
        email_from = SETTINGS.get('HY_LOG_EMAIL_FROM', SETTINGS.get('SMTP_FROM', 'no-reply@service.local'))

        for key in required:
            if not SETTINGS.get(key) or SETTINGS.get(key) == 'not configured':
                self.smtp_warnings.append(
                    f'HY_LOG_TO_EMAIL is enabled, but {key} is missing - no error emails will be sent')
                good_to_go = False

        if not good_to_go:
            return

        recipients = [r.strip() for r in SETTINGS.get('HY_LOG_EMAIL_RECIPIENTS').split(',')]
        verbosity = SETTINGS.get('HY_LOG_EMAIL_VERBOSITY', 'ERROR')

        email_sender = EmailSender()

        # Define and register the custom handler by name for visibility in logging config
        self.logging_config['handlers']['smtp'] = {
            '()': HTMLSMTPHandler,
            'email_sender': email_sender,
            'recipients': recipients,
            'subject': f'Problem encountered with {self.api_name}',
            'email_from': email_from,
            'level': verbosity,
            # 'cooldown_seconds': 60,
            'formatter': 'smtp'
        }

        self.logging_config['root']['handlers'].append('smtp')

        for warning in self.smtp_warnings:
            logging.getLogger('configuration').warning(warning)

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

    def _get_smtp_formater(self):
        # start_env = starting_environment()

        return {
            'datefmt': DATE_FORMAT,
            'style': '{',
            'format': f'''{{asctime}} - {{name}} - {{levelname}} - {{message}}            
{{filename}}:{{lineno}} - {{funcName}}()
 
{{pathname}}
'''
        }
