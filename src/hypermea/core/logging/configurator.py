import logging.config
import os
import platform
import socket

from cerberus import __version__ as cerberus_version
from eve import __version__ as eve_version
from hypermea.core.settings import starting_environment
from hypermea.core import VERSION as hypermea_core_version
from werkzeug.utils import secure_filename

from configuration import SETTINGS, VERSION



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
        if not SETTINGS.has_enabled('HY_LOG_TO_EMAIL'):
            return

        self.smtp_warnings = []
        requires = ['SMTP_HOST', 'SMTP_PORT', 'HY_LOG_EMAIL_RECIPIENTS']
        good_to_go = True
        email_from = SETTINGS.get('HY_LOG_EMAIL_FROM', SETTINGS.get('SMTP_FROM', 'no-reply@service.local'))
        for item in requires:
            if item not in SETTINGS or SETTINGS[item] == 'not configured':
                self.smtp_warnings.append(
                    f'HY_LOG_TO_EMAIL is enabled, but {item} is missing - no error emails will be sent')
                good_to_go = False

        if not good_to_go:
            return

        self.logging_config['handlers']['smtp'] = {
            # TODO: integrate with QueueHandler so email doesn't block
            #       (look at http://flask-logconfig.readthedocs.io/en/latest/ ?)
            'class': 'logging.handlers.SMTPHandler',
            'level': SETTINGS.get('HY_LOG_EMAIL_VERBOSITY'),
            'formatter': 'email',
            'mailhost': [SETTINGS.get('SMTP_HOST'), SETTINGS.get('SMTP_PORT')],
            'fromaddr': email_from,
            'toaddrs': [recipient.strip() for recipient in SETTINGS.get('HY_LOG_EMAIL_RECIPIENTS').split(',')],
            'subject': f'Problem encountered with {self.api_name}'
        }

        self.logging_config['root']['handlers'] += ['smtp']
        self._setup_email_format()


    def _setup_email_format(self):
        if not SETTINGS.has_enabled('HY_LOG_TO_EMAIL'):
            return
        LOG = logging.getLogger('configuration')

        if self.smtp_warnings:
            for warning in self.smtp_warnings:
                LOG.warning(warning)
                return

        instance_name = SETTINGS.get('HY_INSTANCE_NAME')

        email_format = f'''<p>This is a <b>bold</b> statement.</p>
        %(levelname)s sent from {self.api_name} instance "{instance_name}" (hostname: {socket.gethostname()})

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
