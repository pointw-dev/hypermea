import logging
import hypermea.core.logging.setup    # do not remove this import
from hypermea.core.gateway import register
from configuration import SETTINGS
from eve import Eve
from flask_cors import CORS
import hooks


LOG = logging.getLogger('service')


class HypermeaService:
    def __init__(self, **kwargs):
        self._grab_kwargs(kwargs)
        self._name = SETTINGS.get('HY_API_NAME', default_value='{$project_name}')
        self._app = Eve(import_name=self._name)
        CORS(self._app)
        hooks.add_hooks(self._app)

    def _grab_kwargs(self, kwargs):
        self.host = kwargs['host'] if 'host' in kwargs else '0.0.0.0'
        self.debug = False if 'debug' not in kwargs else kwargs['debug'][0] in 'tTyYeE'  # true, yes, enable
        self.threaded = True if 'threaded' not in kwargs else kwargs['threaded'][0] in 'tTyYeE'  # true, yes, enable
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
        border = '-' * (23 + len(self._name))
        LOG.info(border)
        LOG.info(f'****** STARTING {self._name} ******')
        LOG.info(border)
        SETTINGS.dump(callback=LOG.info)
        try:
            register(self._app)
            self._app.run(host=self.host, port=SETTINGS.get('HY_API_PORT'), threaded=self.threaded, debug=self.debug)
        except Exception as ex:  # pylint: disable=broad-except
            LOG.exception(ex)
        finally:
            LOG.info(border)
            LOG.info(f'****** STOPPING {self._name} ******')
            LOG.info(border)

    def stop(self):
        self._app.do_teardown_appcontext()
