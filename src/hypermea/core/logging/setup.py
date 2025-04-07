"""
Configure standard python logging
"""
import os
import socket
import logging.config
import platform

from eve import __version__ as eve_version
from cerberus import __version__ as cerberus_version
from flask.testing import FlaskClient
from hypermea.core import VERSION as hypermea_core_version
from werkzeug.utils import secure_filename

try:
    # this ensures the integration SETTINGS (if they exist) are loaded before the dump
    import integration
except ImportError:
    pass
from configuration import SETTINGS, VERSION, additional_log_configuration


class LogConfigurator:
    def __init__(self, api_name):
        self.api_name = api_name
        self.logging_config = self._set_base_logging_config()
        self._setup_file_logging()
        self._setup_smtp_logging()
        self._prepare_logger()
        self._setup_email_format()

    def _prepare_logger(self):
        logging.config.dictConfig(self.logging_config)
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    def _set_base_logging_config(self):
        return {
        'version': 1,
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        },
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'detail': {
                'format': '%(asctime)s - %(levelname)s - File: %(filename)s - %(funcName)s()'
                          ' - Line: %(lineno)d -  %(message)s'
            },
            'email': {
                'format': f'%(levelname)s sent from {self.api_name} %(asctime)s - '
                          '%(levelname)s - File: %(filename)s - %(funcName)s() - Line: %(lineno)d -  %(message)s'
            }
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

    def _setup_file_logging(self):
        if SETTINGS.has_enabled('HY_LOG_TO_FOLDER'):
            log_folder = SETTINGS.get('FOLDER_TO_LOG_TO')
            if not log_folder:
                log_folder = f'/var/log/{secure_filename(self.api_name)}'
            if not os.path.exists(log_folder):
                os.makedirs(log_folder)

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
        self.smtp_warnings = []
        if SETTINGS.has_enabled('HY_LOG_TO_EMAIL'):
            requires = ['HY_SMTP_HOST', 'HY_SMTP_PORT', 'HY_ERROR_EMAIL_RECIPIENTS', 'HY_ERROR_EMAIL_FROM']
            good_to_go = True
            for item in requires:
                if item not in SETTINGS:
                    self.smtp_warnings.append(
                        f'HY_LOG_TO_EMAIL is enabled, but {item} is missing - no error emails will be sent')
                    good_to_go = False

            if good_to_go:
                self.logging_config['handlers']['smtp'] = {
                    # TODO: integrate with QueueHandler so email doesn't block
                    #       (look at http://flask-logconfig.readthedocs.io/en/latest/ ?)
                    'class': 'logging.handlers.SMTPHandler',
                    'level': 'ERROR',
                    'formatter': 'email',
                    'mailhost': [SETTINGS.get('HY_SMTP_HOST'), SETTINGS.get('HY_SMTP_PORT')],
                    'fromaddr': SETTINGS.get('HY_ERROR_EMAIL_FROM'),
                    'toaddrs': [e.strip() for e in SETTINGS.get('HY_ERROR_EMAIL_RECIPIENTS').split(',')],
                    'subject': f'Problem encountered with {self.api_name}'
                }

                self.logging_config['root']['handlers'] += ['smtp']

    def _setup_email_format(self):
        LOG = logging.getLogger('configuration')
        if self.smtp_warnings:
            for warning in self.smtp_warnings:
                LOG.warning(warning)
        elif SETTINGS.has_enabled('HY_LOG_TO_EMAIL'):  # TODO: can this be moved up to logging_config setup?
            instance_name = SETTINGS.get('HY_INSTANCE_NAME')
            email_format = f'''%(levelname)s sent from {self.api_name} instance "{instance_name}" (hostname: {socket.gethostname()})
    
            %(asctime)s - %(levelname)s - File: %(filename)s - %(funcName)s() - Line: %(lineno)d -  %(message)s
            '''

            # TODO: refactor with SETTINGS.sanitized_settings / core.settings.starting_environment
            email_format += f'''
            {self.api_name} version:       {VERSION}
            hypermea.core version: {hypermea_core_version}
            eve version:           {eve_version}
            cerberus version:      {cerberus_version}
            python version:        {platform.sys.version}
            os_system:             {platform.system()}      
            os_release:            {platform.release()}
            os_version:            {platform.version()}    
            os_platform:           {platform.platform()}  
    
            '''

            SETTINGS.dump(callback=email_format.__add__)
            email_format += '\n\n'

            logger = logging.getLogger()
            handlers = logger.handlers

            smtp_handler = [x for x in handlers if x.name == 'smtp'][0]
            smtp_handler.setFormatter(logging.Formatter(email_format))


def configure_logger():
    api_name = SETTINGS.get('HY_API_NAME')
    LogConfigurator(api_name)
    additional_log_configuration()


configure_logger()
