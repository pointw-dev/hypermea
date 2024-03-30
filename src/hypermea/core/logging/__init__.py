import logging
import json
from .trace.trace_level import TRACE_LEVEL
from .trace.decorators import trace


def _get_console_handler_level():
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.StreamHandler):
            # Assuming the console handler is a StreamHandler
            return handler.level
    return None


def log_request(log, resource, request, lookup, max_body_size):
    requested = resource if resource else 'root'

    current_console_level = _get_console_handler_level()
    if current_console_level is None or current_console_level >= logging.INFO:
        log.info(f'{request.method} request received for {requested}, lookup:{lookup}')
        return

    request_headers = f'{request.headers}'.replace('\n', '\n  ').rstrip()
    if request.is_json:
        request_data = json.dumps(request.json) if request.data else "\"\""
    else:
        request_data = request.data if request.data else "\"\""

    if current_console_level >= logging.DEBUG and len(request_data) > max_body_size:
        request_data = request_data[:max_body_size] + '... [TRACE for full body]'

    log.debug(f'\n{request}\n'
              f'-lookup: {lookup}\n'
              f'-request.values:\n  {request.values.to_dict()}\n'
              f'-request.headers:\n  {request_headers}\n'
              f'-request.data:\n  {request_data}\n')


@trace
def log_response(log, resource, request, payload, max_body_size):
    requested = resource if resource else 'root'

    current_console_level = _get_console_handler_level()
    if current_console_level is None or current_console_level >= 20:
        log.info(f'Response sent for {request} {requested} [{payload.status_code}]')
        return

    response_headers = f'{payload.headers}'.replace('\n', '\n  ').rstrip()
    if payload.is_json:
        response_data = json.dumps(payload.json) if payload.data else "\"\""
    else:
        response_data = payload.data

    if current_console_level >= 10 and len(response_data) > max_body_size:
        response_data = response_data[:max_body_size] + '... [TRACE for full body]'
        if payload.is_json and '_items' in payload.json:
            response_data += f' {len(payload.json["_items"])} items'

    log.debug(f'Response sent for {request} {requested} [{payload.status_code}]\n'
              f'-response.headers:\n  {response_headers}\n'
              f'-payload.data:\n  {response_data}\n')


