import logging
import json
from .trace.trace_level import TRACE_LEVEL
from .trace.decorators import trace
from configuration import SETTINGS

TRUNCATED = '...\n  [Body truncated. Set logging to TRACE for full body, or increase HY_LOG_MAX_BODY_SIZE.]'


def _get_console_handler_level():
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.StreamHandler):
            # Assuming the console handler is a StreamHandler
            return handler.level
    return None


def log_request(log, resource, request, lookup):
    requested = resource if resource else 'root'

    current_console_level = _get_console_handler_level()
    if current_console_level is None or current_console_level >= logging.INFO:
        log.info(f'{request.method} request received for {requested}, lookup:{lookup}')
        return

    request_headers = f'{request.headers}'.replace('\n', '\n  ').rstrip()
    if request.is_json:
        request_body = json.dumps(request.json) if request.data else "\"\""
    else:
        request_body = request.data if request.data else "\"\""

    max_body_size = SETTINGS['HY_LOG_MAX_BODY_SIZE']
    if current_console_level >= logging.DEBUG and len(request_body) > max_body_size:
        request_body = request_body[:max_body_size] + TRUNCATED

    log.debug(f'\n{request}\n'
              f'-lookup: {lookup if lookup else "n/a"}\n'
              f'-request.parameters:\n  {request.values.to_dict()}\n'
              f'-request.headers:\n  {request_headers}\n'
              f'-request.body:\n  {request_body}\n')


@trace
def log_response(log, resource, request, payload):
    requested = resource if resource else 'root'

    current_console_level = _get_console_handler_level()
    if current_console_level is None or current_console_level >= logging.INFO:
        log.info(f'Response sent for {request} {requested} [{payload.status_code}]')
        return

    response_headers = f'{payload.headers}'.replace('\n', '\n  ').rstrip()
    if payload.is_json:
        response_body = json.dumps(payload.json) if payload.data else "\"\""
    else:
        response_body = payload.data

    max_body_size = SETTINGS['HY_LOG_MAX_BODY_SIZE']
    if current_console_level >= 10 and len(response_body) > max_body_size:
        response_body = response_body[:max_body_size] + TRUNCATED
        if payload.is_json and '_items' in payload.json:
            num_items = len(payload.json["_items"])
            response_body += f'\n  Collection has {num_items} {"item" if num_items == 1 else "items"}'

    log.debug(f'Response sent for {request} {requested} [{payload.status_code}]\n'
              f'-response.headers:\n  {response_headers}\n'
              f'-response.body:\n  {response_body}\n')


