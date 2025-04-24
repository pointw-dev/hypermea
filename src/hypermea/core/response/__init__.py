import logging
import traceback
import os
from typing import List, Dict, Optional
from flask import jsonify, make_response, current_app, request, Response, g, after_this_request

LOG = logging.getLogger('hypermea')


unauthorized_message = {
    '_status': 'ERR',
    '_error': {
        'message': 'Please provide proper credentials',
        'code': 401
    }
}

not_found_message = {
    '_status': 'ERR',
    '_error': {
        'message': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.',
        'code': 404
    }
}

def make_error_response(message: str, code: int, issues: Optional[List[Dict]] = None, **kwargs):
    if issues is None:
        issues = []

    if 'exception' in kwargs:
        ex = kwargs.get('exception')
        LOG.error(message, exc_info=ex, stack_info=True)

        tb = traceback.TracebackException.from_exception(ex)
        site_packages_stack = []
        app_stack = []
        hypermea_stack = []
        full_stack = []

        report_stack = True
        separate_stack = True

        for frame in tb.stack:
            path = os.path.relpath(frame.filename)

            stack_item = {
                "line_number": frame.lineno,
                "function": frame.name,
                "code": frame.line.strip() if frame.line else None
            }

            if report_stack:
                if '/hypermea/' in path:
                    stack_item['file'] = 'hypermea/' + path.split('/hypermea/')[1]
                    hypermea_stack.insert(0, stack_item)
                elif 'site-packages' in path:
                    stack_item['file'] = '/site-packages/' + path.split('/site-packages/')[1]
                    site_packages_stack.insert(0, stack_item)
                else:
                    stack_item['file'] = path
                    app_stack.insert(0, stack_item)
            else:
                stack_item['file'] = path
                full_stack.insert(0, stack_item)


        if ex:
            issue = {
                'exception': {
                    'name': type(ex).__name__,
                    'type': ".".join([type(ex).__module__, type(ex).__name__]),
                    'args': ex.args,
                }
            }

            if report_stack:
                if separate_stack:
                    issue.update({
                        'app_stack': app_stack,
                        'hypermea_stack': hypermea_stack,
                        'site_packages_stack': site_packages_stack
                    })
                else:
                    issue.update({'stack': full_stack})

            issues.append(issue)

    resp = {
        '_status': 'ERR',
        '_error': {
            'message': message,
            'code': code
        }
    }

    if issues:
        resp['_issues'] = issues

    return make_response(jsonify(resp), code)



def hal_format_error(data):
    rtn = {
        'status': data.get('_status', "unknown"),
        'status_code': data['_error']['code'],
        'message': data['_error']['message'],
        '_links': {
            "self": request.url
        }
    }

    if '_issues' in data:
        rtn['_embedded'] = {
            "issues": data['_issues']
        }

    return rtn

