# https://pointw-dev.github.io/hypermea/features/runtime-capabilities/logging.html
Feature: Hypermea services create useful logs, configurable to how, what, and where you want to log
    As a DevOps engineer
    I want the logs emitted by the service to provide useful information
      and can be configured how I want
    So that when there are issues I have all the information I need when and where I need it
      to guide me in solving the problem

    By default hypermea services log to console only (visible in the terminal, but also in AWS logs,
    docker logs, etc.) and is set to DEBUG verbosity.  Developers can increase the verbosity to TRACE.

    To also write logs to a file, set HY_LOG_TO_FOLDER.  The default folder is /var/log/your-project-name
    Logs written this way use TimeRotatingFileHander, rolling the log at midnight, keeping 4 backups.

    At deployment time, DevOps can route logs to various sources by verbosity (e.g. all ERRORs
    send an email, or a Teams update).  While the service is running the verbosity can be changed.

    HTTP requests, the heart of a hypermea service, give very detailed information when set to DEBUG and
    very very very detailed information when set to TRACE.  Specifically: DEBUG level HTTP requests emit
      * request details (method, path)
      * the request headers
      * the request body.
    The responses emit
      * response details (status code, reason)
      * response headers
      * the response body
      * the collection count if the response is for a collection resource
    In the event a request body or response body is too large, they will be truncated to HY_LOG_MAX_BODY_SIZE
    bytes (default 1024)
    If your logging verbosity is TRACE, the max body size is ignored and the entire body is logged.

  @slow
  Scenario: Environment details are logged
    Given the service has started
    When I look at the log
    Then I see the versions of important stack components


  Scenario: Base hypermea settings are logged
  Scenario: Settings I created for my service are logged
  Scenario: Turn logging to file on
  Scenario: Choose the file to log to
  Scenario: Override file rolling strategy and its parameters
  Scenario: Change the size after which logged response and request bodies are truncated
  Scenario: TRACE logging ignores max body size
  Scenario: Configure ERROR logs to be sent by email
  Scenario: Configure ERROR logs to be sent to webhook
  Scenario: Adding my own logging.yml file overrides and extends the built-in logging behaviour
  Scenario: My application fails to handle an exception

# May need to postpone integration settings logging until after #90
  Scenario: Integration settings are logged
