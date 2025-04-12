import logging

from tests import *
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that


import io
from multiprocessing import Process, Queue, Event
import signal
import time
from contextlib import redirect_stdout, redirect_stderr

import settings


FEATURE = 'hypermea/enhanced_logging.feature'


class QueueLogHandler(logging.Handler):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def emit(self, record):
        self.queue.put((
            record.name,
            record.levelname,
            self.format(record)
        ))


def prepare_logger(q):
    log_handler = QueueLogHandler(q)
    log_handler.setFormatter(logging.Formatter('%(message)s'))
    root_logger = logging.getLogger()
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.INFO)


@given('the service has started')
def given_the_service_has_started(context, service):
    def start_the_service(q, stop_event):
        def handle_shutdown(signum, frame):
            service.stop()
            if context.process.is_alive():
                context.process.terminate()
                context.process.join()

        signal.signal(signal.SIGINT, handle_shutdown)
        signal.signal(signal.SIGTERM, handle_shutdown)

        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            try:
                import threading

                def run_app():
                    service.start()

                prepare_logger(q)
                thread = threading.Thread(target=run_app)
                thread.start()

                # Wait for Flask to fully start
                ready_phrases = ["* Serving Flask app", "* Debug mode:"]
                max_wait = 10
                start_time = time.time()

                while time.time() - start_time < max_wait:
                    out = f.getvalue()
                    if all(phrase in out for phrase in ready_phrases):
                        q.put(('status', 'READY'))
                        break
                    time.sleep(0.1)
                else:
                    q.put(('status', 'TIMEOUT'))
                    return

                # start listening for the stop signal
                while not stop_event.is_set():
                    time.sleep(0.2)

            except Exception:
                pass

        q.put(f.getvalue())

    context.queue = Queue()
    context.stop_event = Event()
    context.process = Process(target=start_the_service, args=(context.queue, context.stop_event), daemon=True)
    context.process.start()


@given('the service is configured with file logging enabled')
def given_the_service_is_configured_with_file_logging_enabled(deploy_time_settings):
    deploy_time_settings.logging.log_to_folder = True


@when('I look at the log')
def when_i_look_at_the_console(context):
    context.stop_event.set()
    context.process.join(timeout=0.2)

    log_entries = []

    try:
        while True:
            log_entries.append(context.queue.get_nowait())
    except Exception:
        pass

    context.log_entries = log_entries


@then('I see the versions of important stack components')
def then_i_see_the_versions_of_important_stack_components(context):
    stack_lines = [line for line in context.log_entries if line[0] == 'environment']
    assert_that(len(stack_lines)).is_greater_than(0)

    service_name = settings.hypermea.service_name
    missing = [
        component for component in [service_name, 'eve', 'cerberus', 'python', 'os_system', 'os_release', 'os_version', 'os_platform']
        if not any(msg.startswith(component) for _, _, msg in stack_lines)
    ]
    assert_that(missing).described_as("Missing version logs for").is_empty()


@then('I see the base settings for hypermea')
def then_i_see_the_base_settings_for_hypermea(context):
    deploy_time_settings = [entry for entry in context.log_entries if entry[0] == 'service' and entry[2].startswith('HY_')]
    assert_that(len(deploy_time_settings)).is_greater_than(0)

    missing = [
        setting for setting in ['HY_SERVICE_NAME', 'HY_SERVICE_PORT', 'HY_PAGINATION_DEFAULT']
        if not any(msg.startswith(setting) for _, _, msg in deploy_time_settings)
    ]
    assert_that(missing).described_as("Missing version logs for").is_empty()
