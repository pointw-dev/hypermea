import os
import logging
import hypermea.core.logging.setup    # do not remove this import
from hypermea.core import HypermeaEve
from hypermea.core.gateway import register
from configuration import SETTINGS
from flask_cors import CORS
import hooks


LOG = logging.getLogger('service')

import logging
import platform

from eve import __version__ as eve_version
from cerberus import __version__ as cerberus_version
from hypermea.core import VERSION as hypermea_core_version
from configuration import SETTINGS, VERSION as api_version

def dump_starting_details():
    logger = logging.getLogger("environment")
    LOG.info("== stack versions")

    api_name = SETTINGS.get("HY_API_NAME", "api")

    components = {
        api_name: api_version,
        "hypermea.core": hypermea_core_version,
        "eve": eve_version,
        "cerberus": cerberus_version,
        "python": platform.sys.version,
        "os_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "os_platform": platform.platform(),
    }

    max_key_length = max(len(k) for k in components.keys())

    for name, version in components.items():
        padding = " " * (max_key_length - len(name) + 1)
        logger.info(f"{name}{padding}{version}")

    SETTINGS.dump(callback=LOG.info)



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
        # reload [y/n]          Enable or disable the reloader
        # debugger [y/n]        Enable or disable the debugger
        # eager-loading [y/n]
        # extra-files           ; sep list of files that trigger reload
        # exclude-pattern       ; sep list of fnmatch pattersn
        pass

    def start(self):
        self.starting_banner()
        dump_starting_details()

        try:
            register(self._app)
            self._app.run(host=self.host, port=SETTINGS.get('HY_API_PORT'), threaded=self.threaded, debug=self.debug)
        except Exception as ex:  # pylint: disable=broad-except
            LOG.exception(ex)
        finally:
            self.stopping_banner()

    def stop(self):
        self._app.do_teardown_appcontext()
