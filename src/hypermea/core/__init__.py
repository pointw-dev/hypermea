# do not change version manually
VERSION = '0.9.41'

from eve import Eve
from eve.flaskapp import EveWSGIRequestHandler

class HypermeaWSGIRequestHandler(EveWSGIRequestHandler):
    """Extend werkzeug request handler to include current Eve version in all
    responses, which is super-handy for debugging.
    """

    @property
    def server_version(self):
        return (
            "hypermea/%s " % VERSION
            + super().server_version
        )

class HypermeaEve(Eve):
    def run(self, host=None, port=None, debug=None, **options):
        """
        Pass our own subclass of :class:`werkzeug.serving.WSGIRequestHandler
        to Flask.
        """

        options.setdefault("request_handler", HypermeaWSGIRequestHandler)
        super().run(host, port, debug, **options)
