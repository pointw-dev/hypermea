# Enhanced Logging

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

* `TRACE` level
    * use as you wish (`LOG.trace('very verbose message here')`)
    * Use `@trace` decorator to automatically log a function's enter and exit (even if exception is thrown)
    * Disable with `HY_TRACE_LOGGING` to avoid stepping into the detailed logger when debugging (disabled by default in your `_env.conf`)
* Environment / settings at the beginning of each run
```text
2025-04-03 20:26:41,733 - configuration - INFO - my-api version           1.0.3
2025-04-03 20:26:41,733 - configuration - INFO - hypermea-core version    0.9.50
2025-04-03 20:26:41,733 - configuration - INFO - eve version              2.2.0
2025-04-03 20:26:41,733 - configuration - INFO - cerberus version         1.3.7
2025-04-03 20:26:41,733 - configuration - INFO - python version           3.12.3 (main, May 17 2024, 12:24:17) [GCC 13.2.0]
2025-04-03 20:26:41,733 - configuration - INFO - os_system version        Linux
2025-04-03 20:26:41,733 - configuration - INFO - os_release version       6.11.0-21-generic
2025-04-03 20:26:41,733 - configuration - INFO - os_version version       #21~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Feb 24 16:52:15 UTC 2
2025-04-03 20:26:41,734 - configuration - INFO - os_platform version      Linux-6.11.0-21-generic-x86_64-with-glibc2.39
2025-04-03 20:26:41,818 - service - INFO - -----------------------------
2025-04-03 20:26:41,818 - service - INFO - ****** STARTING my-api ******
2025-04-03 20:26:41,818 - service - INFO - -----------------------------
2025-04-03 20:26:41,818 - service - INFO - == HY: HypermeaService base configuration
2025-04-03 20:26:41,818 - service - INFO - HY_ADD_ECHO: Disabled
2025-04-03 20:26:41,818 - service - INFO - HY_API_NAME: dev-hypermea-api
2025-04-03 20:26:41,818 - service - INFO - HY_API_PORT: 2112
2025-04-03 20:26:41,818 - service - INFO - HY_CACHE_CONTROL: no-cache, no-store, must-revalidate
2025-04-03 20:26:41,818 - service - INFO - HY_CACHE_EXPIRES: 30
2025-04-03 20:26:41,818 - service - INFO - HY_INSTANCE_NAME: opus
2025-04-03 20:26:41,818 - service - INFO - HY_LOG_MAX_BODY_SIZE: 1024
2025-04-03 20:26:41,818 - service - INFO - HY_LOG_TO_FOLDER: Disabled
2025-04-03 20:26:41,818 - service - INFO - HY_MONGO_ATLAS: Disabled
2025-04-03 20:26:41,818 - service - INFO - HY_MONGO_DBNAME: dev-hypermea-api
2025-04-03 20:26:41,818 - service - INFO - HY_MONGO_HOST: localhost
2025-04-03 20:26:41,818 - service - INFO - HY_MONGO_PORT: 27017
2025-04-03 20:26:41,818 - service - INFO - HY_PAGINATION_DEFAULT: 1000
2025-04-03 20:26:41,818 - service - INFO - HY_PAGINATION_LIMIT: 3000
2025-04-03 20:26:41,818 - service - INFO - HY_SEND_ERROR_EMAILS: Disabled
2025-04-03 20:26:41,818 - service - INFO - HY_TRACE_LOGGING: Disabled

```  

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