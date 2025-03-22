# Miscellaneous scaffolding features

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::


* WARNING when combining query string parameters with curl, surround URL in quotes (else & is parsed by bash)

* Settings/configuration system
  * The `HypermeaService` ships with a sophisticated settings/configuration management system based on these principles:
    * Easy to run: An API should run right out of the box without requiring configuration
    * Container compatible: All settings can be set with environment variables.
    * Developer convenience:  Developers can easily modify settings without accidentally commiting code with experimental values.
      * use `_env.conf` to set these values - included when your API was created
      * This file is in `.gitignore` and `.dockerignore` so it will never accidentally be shipped anywhere but your dev environment
  * Visible:  all setting values are logged at startup and can be viewed with `GET /_settings` - no more wondering what value was set when debugging a problem at 3:00 AM
  * yte - Yes, True, Enabled (case insensitive)

  * (TODO: cancellable, optional, prefix stuff?,  `settings.has_enabled()`   [0] == 'YyTtEe')


* test suite (BDD/pytest-bdd)
  * separate hypermea folder from your application folder
  * test_debug_display_environment
  * allure
  * requires mongo, but runs independently 
    * i.e. separate MongoDB db, separate Redis db
    * can run tests even if service is also running

```ini
[pytest]
addopts = -v -m "not skip"
testpaths = __tests__
bdd_features_base_dir = ../features

markers =
    slow: this feature/scenario runs slowly (deselect with '-m "not slow"')
    skip: skip this feature/scenario
    wip: this feature/scenario is under development (deselect with '-m "not wip"')
    only: if you want to run only these tests select with '-m only'

filterwarnings =
    ignore::pytest.PytestDeprecationWarning
    ignore::DeprecationWarning
```


* HAL media type
  * Eve's out-of-box JSON structure is very close to HAL.  With hypermea, you get even closer
    * Content-type is `application/hal+json`
    * `_links` are tidied up, some superfluous metadata is removed
    * hierarchical navigation follows IANA conventions
    * (this is constantly improving - coming soon curies, _embedded, as well as other standard hypermedia types like Siren, Atom, Collection+JSON, etc.)
    * https://dev.to/nevnet99/wtf-is-hal-hypertext-application-language-2fo6

* X-Total-Count (useful with HEAD request, `curl -I --head localhost:2112`)
* links-only
* _query_options

* Exception Handling
  * improves on Eve's out-of-box behaviour by standardizing the error response - even in the case of 5xx's
  `{_status: "ERR", _error: {code:422, message: ""}, _issues: [] }`
  * your code can call `utils.make_error_response()` to emit custom error messages that follow this standard.

* enforced pluralization
  * collections are pluralized
  * items are singularized

* CORS permissively set by default

* create_form / edit_form (RFC 6861)

* common fields

```python
COMMON_FIELDS = {
    '_owner': {'type': 'string'},
    '_tags': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    '_x': {
        'allow_unknown': True
    }
}
```
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
