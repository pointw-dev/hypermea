---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
# Just The Docs:            https://just-the-docs.com/
layout: home
---

# Simple Commands, Serious APIs
Transform your development workflow with **hypermea**, the toolkit that lets you rapidly create production-ready hypermedia-driven APIs.  Equipped with advanced features, sophisticated error handling, expressive logging and much more, hypermea ensures your APIs are built to last, whether for small projects or enterprise-scale solutions.  Discover the power of hypermedia APIs and how **hypermea makes it easy**.

# Features

This section is under heavy construction.  In no particular order...

## Settings/configuration system

The `HypermeaService` ships with a sophisticated settings/configuration management system based on these principles:

* Easy to run: An API should run right out of the box without *requiring* configuration
* Container compatible: All settings can be set with environment variables, and thus set via `docker-compose.yml` or kubernetes Deployment.
* Developer convenience:  Developers can easily modify settings without accidentally commiting code with experimental values.
  * use `_env.conf` to set these values - included when your API was created
  * This file is in `.gitignore` and `.dockerignore` so it will never accidentally be shipped anywhere but your dev environment
* Visible:  all setting values are logged at startup and can be viewed with `GET /_settings` - no more wondering what value was set when debugging a problem at 3:00 AM
* Organized: by base, by api, by integration (with prefixes)

(TODO: cancellable, optional, prefix stuff?,  `settings.has_enabled()`   [0] == 'YyTtEe')

## Logging

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

## Echo

Sometimes you need to test a client's ability to respond to various message or error/status codes.  It may be difficult to purposefully generate a 500.  In these cases you can enable `HY_ADD_ECHO`.  Then you can PUT to `/_echo` a JSON as follows:

```json
{
  "status_code": ###,
  "message": {...}
}
```

This produce a response with status code as specified, with the `message` value as the body.  It also goes through the service logging system, so you can test receiving emails on 5xx, etc. (or however you choose to extend the logging)

## Exception Handling

* improves on Eve's out-of-box behaviour by standardizing the error response - even in the case of 5xx's
  `{_status: "ERR", _error: {code:422, message: ""}, _issues: [] }`
* your code can call `utils.make_error_response()` to emit custom error messages that follow this standard.

HAL media type

* Eve's out-of-box JSON structure is very close to HAL.  With hypermea, you get even closer
  * Content-type is `application/hal+json`
  * `_links` are tidied up, some superfluous metadata is removed
  * hierarchical navigation follows IANA conventions
  * (this is constantly improving - coming soon curies, _embedded, as well as other standard hypermedia types like Siren, Atom, Collection+JSON, etc.)

## API Gateway Registration

(details)

## Miscellaneous

* enforced pluralization

  * collections are pluralized
  * items are singularized

* CORS permissively set by default

* create_form / edit_form (RFC 6861)

* `utils.get_db()` to quickly access the mongodb collections

* `utils.get_api()` to make http requests in your code to the API itself

* hypermea errorlevels / exit codes:
  1 - not run in API folder structure
  2 - an API already exists in this folder
  3 - user cancelled when folder is not empty
  11 - --set-version value not specified correctly

  10x - git
  101 - git already added

  20x - auth
  201 - auth already added
  
  30x - validation
  301 - validation already installed
  
  40x - docker
  401 - docker already installed
  
  50x - websocket
  501 - websocket already installed
  
  60x - serverless
  601 - serverless already added
  602 - node not installed
  603 - serverless not installed
  604 - node not initialized
  605 - serverless plugin not installed
  666 - serverless installation canceled by user
  
  70x - resource
  701 - resource name invalid 
  702 - resource already exists
  703 - resource does not exist
  704 - could not delete resource files
  
  80x - link
  801 - link already exists
  802 - local resource does not exist
  803 - both parent and child of a link cannot be remote (at least one must be local)
  804 - link does not exist
  
  90x - integration
  901 - integration already exists
  902 - name required when choosing empty integration

 100x - affordances
 1001 - affordance already exists
 1002 - affordance does not exist
 1003 - cannot attach affordance to a resource that does not exist
 1004 - affordance already attached 

  

* organized folder structure
  - designed with more than simple api in mind (e.g. scripts)
  - src, doc, etc
  - FAQ why my-api/src/my-api ?
  - domain decomposition
  - hooks

  - integrations
  - affordances
  - (addins: validation, authorization, etc...)

* common.py

  _x
  name
  description
  
* halchemy
