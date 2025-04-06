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
    Given the service has started
    When I look at the log
    Then I see the base settings for hypermea

  Scenario: Settings I created for my service are logged
    Given I have configured settings that custom to my service
    And the service has started
    When I look at the log
    Then I see my service custom settings

  Scenario: Sensitive settings are redacted in the log
    Given I have configured a setting for a password
    And the service has started
    When I look at the log
    Then I do not see the secret values



  Scenario: Change the size after which logged response and request bodies are truncated
  Scenario: TRACE logging ignores max body size

  Scenario: Configure logs to be sent by email
  Scenario: Configure logs to be sent to webhook
  Scenario: Adding my own logging.yml file overrides and extends the built-in logging behaviour


# May need to postpone integration settings logging until after #90
  Scenario: Integration settings are logged


# The scenario functions for the last two are named SKIP_* so they won't fire
# it turns out wiring up a fs mock is tricky given how the log setup is currently
# implemented.  These two scenarios have passed integration testing, but for now
# they will not be tested in this feature suite.  You can still view the step
# definitions - but as they are currently defined they will write to your hard
# drive if you run them.
  Scenario: Enable logging to file
    Given the service is configured with file logging enabled
    When the client does something that causes log events to occur
    Then the log is written to the default location

  Scenario: Choose the folder to log to
    Given the service is configured with file logging enabled
    And the log folder is specified
    When the client does something that causes log events to occur
    Then the log is written to the specified location


