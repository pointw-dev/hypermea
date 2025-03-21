# Logging

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

* out of the box, the python logging module is configured with
    * TRACE level
        * use as you wish (`LOG.trace('very verbose message here')`)
        * Use `@trace` decorator to automatically log a function's enter and exit (even if exception is thrown)
        * Disable with HY_TRACE_LOGGING to avoid stepping into the detailed logger when debugging (disabled by default in your `_env.conf`)
    * Enable `HY_LOG_TO_FOLDER` and logs are created in `/var/logs/service-name`  (which the dev `docker-compose.yml` maps to local volume so you can view the logs even if the container is stopped)
    * You can be notified by email if the server sends a 5xx response
        * Enable `HY_SEND_ERROR_EMAILS`
        * then configure `HY_SMTP_PORT`, `HY_SMTP_SERVER`, `HY_ERROR_EMAIL_RECIPIENTS`, and `HY_ERROR_EMAIL_FROM`
    * View and change the logging verbosity at runtime with a GET and/or PUT to `/_logging`  (provide details)
* Easily extend the logging capabilities using the standard Python `logging` modules
    * Publish to Slack on 5xx, or whatever circumstance you wish (the 500th GET to a particular resource? - only limit is your imagination)
    * See and modify `utils/log_setup.py`

* request and response details when DEBUG is set
  * [Body truncated. Set logging to TRACE for full body, or increase HY_LOG_MAX_BODY_SIZE.]
  * Collection has 5 items


* change logging verbosity at run-time:  
  * From the root document, follow the `logging` link relation and 
    * GET to see the current logging verbosity,
    ```json
    {"console":"DEBUG"}
    ```
    * change it then PUT it back