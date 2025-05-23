# Hypermea Core Library
:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

## Introduction

The core library is used by the hypermea toolkit.  It is not intended to be used by itself (though if you know what you are doing, you could).

When you create an API using hypermea, this library is automatically installed and is available for you to use.

Please see [hypermea](https://github.com/pointw-dev/hypermea) for the full toolkit and documentation.

## The core library

The core library consists of the following modules.  These are all wired up in your API when you created it using hypermea.  Some parts of the library provide useful functions to API developers.  Others are intended for internal use and will not likely be useful to you directly.

### Useful

#### hypermea.core.utils

details

* get_api() -> flask.testing.FlaskClient
* get_db() -> pymongo.database.Database
* is_mongo_running() -> bool (coming soon)

Note: the `log_setup.py` under `utils` is used to set up logging and has no uses for your API

#### validation

Describe the `HypermeaValidator`, used to add the following validations and types, as well as inheritable to extend:

validations

* unique_ignorecase
* unique_to_parent
* unique_to_owner (coming soon)
* remote_relation (coming soon)

types

* iso_date
* iso_time
* iso_duration

(link to Eve doc for more info on extending)

#### logging

background explanation, mention the addition to the standard python logging

* configures
    * standard formatting,
    * logging errors to SMTP (`HY_LOG_TO_EMAIL`),
    * logging to folder (`HY_LOG_TO_FOLDER`) - doco details (timed rotation at midnight, etc.)
* the TRACE level accessible with `LOG.trace()`
* the `@trace` decorator (enabled by default, disable by setting `HY_TRACE_LOGGING` to disable)

reference how to adjust the logging verbosity level in the hypermea docs

#### settings

details: singleton, pulls from environment variables, overridable with `_env.conf`, etc. (note no underscores in prefix)

* create(prefix: str, setting_name: str, default_value: str = None, is_optional: bool = False)
* set_prefix_description(prefix: str, description: str)
* has_enabled(setting_name: str) -> bool
* dump(prefix: str = None, callback: Optional[Callable[[str], None]] = None)
* get(setting_name: str, default_value: str = None)
* []

### Not ones you will likely use directly

#### affordances

details

#### gateway

details

#### hooks

details

#### render

details

#### clean_href()

details
