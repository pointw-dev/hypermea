import types
from typing import Any
import logging
import pytest
from pymongo import MongoClient
from hypermea_service import HypermeaService

import os, sys

LOG = logging.getLogger('pytest')
logger = logging.getLogger()
handler = [x for x in logger.handlers if x.name == 'console'][0]
handler.setLevel(getattr(logging, 'WARNING'))


def load_settings_from_file(filename):
    d = types.ModuleType('settings')
    with open(filename) as f:
        exec(f.read(), d.__dict__)
    return {k: v for k, v in d.__dict__.items() if k.isupper()}


@pytest.fixture
def hypermea_settings() -> dict[str, str]:
    return {
        'HY_API_PORT': '2113',
        'HY_MONGO_DBNAME': 'pytest',
        'HY_TRACE_LOGGING': 'Disabled',
        'HY_CACHE_CONTROL': 'no-cache, no-store, must-revalidate',
        'HY_CACHE_EXPIRES': '30',
    }


@pytest.fixture
def eve_settings() -> dict[str, Any]:
    return {}


@pytest.fixture
def api(hypermea_settings, eve_settings):
    # allow step definitions to change hypermea settings
    for key, value in hypermea_settings.items():
        os.environ[key.upper()] = value

    # allow step definitions to change eve settings
    settings_filename = os.path.join(os.path.dirname(__file__), '../settings.py')
    test_settings = load_settings_from_file(settings_filename)
    for key, value in eve_settings.items():
        test_settings[key.upper()] = value

    service = HypermeaService(host='0.0.0.0', debug='Enabled', settings=test_settings)
    service.dump_settings()
    app = service._app

    def setup_database():
        pass

    def cleanup_database():
        connection = MongoClient(
            app.config.get('MONGO_HOST'), app.config.get('MONGO_PORT')
        )
        connection.drop_database(app.config.get('MONGO_DBNAME'))
        connection.close()

    cleanup_database()
    setup_database()

    yield app.test_client()

    cleanup_database()
