import importlib.util
import logging
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
    import settings

    host = settings.mongo.host
    port = settings.mongo.port
    # TODO: ensure this works with atlas, or other permutations
    try:
        with socket.create_connection((host, port), timeout=0.5):  # TODO: configurable???
            return True
    except OSError:
        return False


def get_logging_handler_by_name(name: str) -> logging.Handler:
    handler_map = {h.name: h for h in logging.getLogger().handlers if hasattr(h, 'name')}
    return handler_map[name]


def get_singular_plural(word):
    import inflect

    if ',' in word:
        # ASSERT word.count(',') == 1
        a = word.split(',')
        return a[0], a[1]

    p = inflect.engine()

    singular = word if not p.singular_noun(word) else p.singular_noun(word)
    plural = word if p.singular_noun(word) else p.plural_noun(word)

    if singular == plural:  # in case of words like moose, fish
        plural = plural + 's'

    return singular, plural


def import_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
