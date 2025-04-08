import socket

from flask import current_app
from flask.testing import FlaskClient
from pymongo.database import Database
from .singleton import Singleton
from .emoji import LEVEL_EMOJIS, EmojiFormatter


def get_db() -> Database:
    return current_app.data.driver.db


def get_api() -> FlaskClient:
    return current_app.test_client()


def is_mongo_running() -> bool:
    from configuration import SETTINGS

    host = SETTINGS['HY_MONGO_HOST']
    port = SETTINGS['HY_MONGO_PORT']
    # TODO: ensure this works with atlas, or other permutations
    try:
        with socket.create_connection((host, port), timeout=0.5):  # TODO: configurable???
            return True
    except OSError:
        return False


