import sys
import os
import logging
from pathlib import Path
from typing import Any

#### Ensure src/service is on sys.path to enable 'from settings import ...'
service_dir = Path(__file__).resolve().parents[1] / "service"
sys.path.insert(0, str(service_dir))
####

import pytest
from pymongo import MongoClient

from hypermea.core.utils import is_mongo_running

from settings import HypermeaSettings
from settings.all_settings import AllSettings, inject_settings, reset_settings, build_settings
from integration.mongo.settings import MongoSettings

from tests import load_settings_from_file
os.environ["HYPERMEA_DISABLE_SETTINGS_AUTOLOAD"] = "1"


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    if not is_mongo_running():
        pytest.exit("❌ Could not connect to MongoDB instance.  Aborting.")


@pytest.fixture(scope='module')
def dev_time_settings() -> dict[str, Any]:
    return {
        'OPTIMIZE_PAGINATION_FOR_SPEED': False
    }

@pytest.fixture(scope='function')
def deploy_time_settings() -> AllSettings:
    return build_settings(
        hypermea=HypermeaSettings(service_port=1999),
        mongo=MongoSettings(dbname="pytest")
    )

@pytest.fixture(scope='function')
def service(deploy_time_settings: AllSettings, dev_time_settings):
    inject_settings(deploy_time_settings)
    service = service_with_test_starting_environment(dev_time_settings)
    app = service._app

    def setup_database():
        pass  # prepare initial state if needed

    def cleanup_database():
        connection = MongoClient(app.config.get('MONGO_HOST'), app.config.get('MONGO_PORT'))
        connection.drop_database(app.config.get('MONGO_DBNAME'))
        connection.close()

    cleanup_database()
    setup_database()

    yield service

    cleanup_database()
    reset_settings()

@pytest.fixture(scope='function')
def api(service):
    with service._app.test_client() as api:
        yield api


def service_with_test_starting_environment(dev_time_settings):
    # Load Eve-specific settings
    import os
    settings_filename = os.path.join(os.path.dirname(__file__), '../service/static_settings.py')
    settings_file_contents = load_settings_from_file(settings_filename)

    for key, value in dev_time_settings.items():
        settings_file_contents[key.upper()] = value

    from hypermea_service import HypermeaService

    logger = logging.getLogger()
    handler = [x for x in logger.handlers if x.name == 'console'][0]
    handler.setLevel(logging.WARNING)

    service = HypermeaService(
        host='0.0.0.0',
        debug='Disabled',
        settings=settings_file_contents,
        threaded='Disabled',
        use_reloader='Disabled'
    )

    return service
