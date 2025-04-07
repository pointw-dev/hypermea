import hypermea.core.logging.setup    # do not remove this import

import os
import logging
from hypermea.core import HypermeaEve
from hypermea.core.gateway import register
from hypermea.core.logging import log_starting_environment
from flask_cors import CORS
import hooks
from hypermea.core.logging import log_starting_environment
from configuration import SETTINGS

LOG = logging.getLogger('service')


class HypermeaService:
    def __init__(self, **kwargs):
        self._grab_kwargs(kwargs)
        self._name = SETTINGS.get('HY_API_NAME', default_value='dev-hypermea-api')
        settings = os.path.join(os.path.dirname(__file__), 'settings.py')
        if 'settings' in kwargs:
            settings = kwargs['settings']
        self._app = HypermeaEve(import_name=self._name, settings=settings)
        CORS(self._app)
        hooks.add_hooks(self._app)
        self.border = '-' * (23 + len(self._name))

    def starting_banner(self):
        LOG.info(self.border)
        LOG.info(f'****** STARTING {self._name} ******')
        LOG.info(self.border)

    def stopping_banner(self):
        LOG.info(self.border)
        LOG.info(f'****** STOPPING {self._name} ******')
        LOG.info(self.border)

    def _grab_kwargs(self, kwargs):
        self.host = kwargs['host'] if 'host' in kwargs else '0.0.0.0'
        self.debug = False if 'debug' not in kwargs else kwargs['debug'][0] in 'tTyYeE'  # true, yes, enable
        self.threaded = True if 'threaded' not in kwargs else kwargs['threaded'][0] in 'tTyYeE'  # true, yes, enable
        self.use_reloader = True if 'use_reloader' not in kwargs else kwargs['use_reloader'][0] in 'tTyYeE'  # true, yes, enable
        # port
        # cert                  Specify a certificate file to use HTTPS
        # key                   The key file to use when specifying a cert
        # eager-loading [y/n]
        # extra-files           ; sep list of files that trigger reload
        # exclude-pattern       ; sep list of fnmatch pattersn
        pass

    def start(self):
        self.starting_banner()
        log_starting_environment()

        try:
            register(self._app)
            self._app.run(host=self.host, port=SETTINGS.get('HY_API_PORT'), threaded=self.threaded, debug=self.debug)
        except Exception as ex:  # pylint: disable=broad-except
            LOG.exception(ex)
        finally:
            self.stopping_banner()

    def stop(self):
        self._app.do_teardown_appcontext()
