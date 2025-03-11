# {$project_name}

Created with **[hypermea](https://pointw-dev.github.io/hypermea/)**.

## Getting Started

To launch the service (I recommend you first create a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/)):

```bash
hypermea run
```

If you have created this api with docker support (`hypermea api create {$project_name} --add-docker`) then to launch the service with docker-compose:

`docker compose up -d`

If you have created this api with serverless support (`hypermea api create {$project_name} --add-serverless`) then launch with:

`sls wsgi serve -p 2112`


Either way, the API is now running and its base endpoint is

http://localhost:2112


After making changes to the API, you must stop/start the API service.

## Configuration

The API is configured via environment variables.  These can be set in in several ways:

* Your OS

  * `set var=value` in Windows
  *  `export var=value` in Linux

* In `docker-compose.yml`

  ```yml
  environment:
   - var1=value1
   - var2=value2
  ```

* In serverless-XXX.yml

  ```yml
  environment:
    var1: value1
    var2: value2
  ```

* In `_env.conf` (this is useful to set values for use in your IDE, this file is listed in `.gitignore` and `.dockerignore` - lines that begin with `#` are treated as comments)  Takes precedence over OS envars.

  ```bash
  var1=value1
  var2=value2
  ```

The base variables are prefixed with HY_ .  The environment variables you can set are:

| Variable                  | Description                                                  | Default                                                     |
| ------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| HY_API_NAME               | The name of your API.  Appears in logs and emails.           | The name you used with `hypermea api create` (i.e. {$project_name})                              |
| HY_MONGO_ATLAS            | Set to Enabled (or True, or Yes) to use the following Mongo values to construct the MONGO_URI.  If disabled, will use a non-Atlas connection. | Disabled                                                    |
| HY_MONGO_HOST             |                                                              | localhost                                                   |
| HY_MONGO_PORT             | (ignored if HY_MONGO_ATLAS is enabled)                       | 27017                                                       |
| HY_MONGO_DBNAME           |                                                              | The name you used with `hypermea api create` (i.e. {$project_name})                             |
| HY_API_PORT               |                                                              | 2112                                                        |
| HY_INSTANCE_NAME          | This name appears in logs and in error emails                | The hostname the API is running on (`socket.gethostname()`) |
| HY_TRACE_LOGGING          | When enabled, causes logs to include enter/exit/exception details for each method - not something to have enabled in production. | Enabled                                                     |
| HY_PAGINATION_LIMIT       | Eve pass-through                                             | 3000                                                        |
| HY_PAGINATION_DEFAULT     | Eve pass-through                                             | 1000                                                        |
| HY_LOG_TO_FOLDER          | (disable if deploying as serverless as there is no folder to log to) | Enabled                                                     |
| HY_SEND_ERROR_EMAILS      | (only works if the following values are set)                 | Enabled                                                     |
| HY_SMTP_HOST              |                                                              | internal.cri.com                                            |
| HY_SMTP_PORT              |                                                              | 25                                                          |
| HY_ERROR_EMAIL_RECIPIENTS |                                                              | michael@pointw.com                                          |

Optional environment variables

| Variable             | Description                             |
| -------------------- | --------------------------------------- |
| HY_MONGO_USERNAME    | (required if HY_MONGO_ATLAS is enabled) |
| HY_MONGO_PASSWORD    | (required if HY_MONGO_ATLAS is enabled) |
| HY_MONGO_AUTH_SOURCE | Eve pass-through                        |
| HY_MEDIA_BASE_URL    | Eve pass-through                        |
| HY_PUBLIC_RESOURCES  | not yet implemented                     |
| HY_URL_PREFIX        | If the API will be deployed behind a URL with a path, use this variable to set that path.  For example, if you deploy the API behind https://example.com/api/my_service, then set HY_URL_PREFIX to "api/my_service" |
| HY_CACHE_CONTROL     | Sets the Cache-Control header (e.g. `no-cache, no-store, must-revalidate`) |
| HY_CACHE_EXPIRES     | Sets the Cache-Expires header (value is in secods)           |
| HY_ADD_ECHO          | If enabled, an undocumented endpoint will be created whose relative path is `/_echo`.  PUT {"message": {}, "status_code: int"} to this endpoint and it will be echoed back to you and logged (`.info` if < 400, `.warning` if < 500, else `.error`).  Useful to test the behaviour of error codes (e.g. with logging configurations) |


If using auth (e.g. `hypermea api create {$project_name} --add-auth` )

| Variable               | Description                                                  | Default                                          |
|------------------------| ------------------------------------------------------------ | ------------------------------------------------ |
| AUTH_ADD_BASIC         | When enabled, allows a basic authentication scheme with root/password | No                                               |
| AUTH_ROOT_PASSWORD     | When AUTH_ADD_BASIC is enabled, this is the password the root user uses to gain access to the API. | password                                         |
| AUTH_REALM             | Appears in the `WWW-Authenticate` header in unauthorized requests. | {$project_name}.pointw.com                       |
| AUTH_JWT_DOMAIN        |                                                              | {$project_name}.us.auth0.com                     |
| AUTH_JWT_AUDIENCE      | This is the identifier a client uses when requesting a token from the auth provider.  It is a URI only (identifier only), not an actual URL (i.e. no requests are made to it) | https://pointw.com/{$project_name}               |
| AUTH0_API_AUDIENCE     | When {$project_name} requests a token to use the Auth0 API, this is the audience for the token. | https://{$project_name}.us.auth0.com/api/v2/     |
| AUTH0_API_BASE_URL     | The base of the Auth0 API                                    | https://{$project_name}.us.auth0.com/api/v2      |
| AUTH0_CLAIMS_NAMESPACE | If you configure Auth0 to insert additional claims, use this value as a namespace (prefix). | https://pointw.com/{$project_name}               |
| AUTH0_TOKEN_ENDPOINT   | When {$project_name} needs to call the Auth0 API, it uses this endpoint to request a token. | https://{$project_name}.us.auth0.com/oauth/token |
| AUTH0_CLIENT_ID        | When {$project_name} needs to call the Auth0 API, it uses this client id/secret to authenticate.  These are not the client id/secret of your application. | --your-client-id--                               |
| AUTH0_CLIENT_SECRET    |                                                              | --your-client-secret--                           |

## Project Structure

| File                            | Description                                                                                                                                                                                                                                                         |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| hypermea_service.py                  | Defines the HypermeaService class, the http server that powers the API.                                                                                                                                                                                             |
| run.py                          | Instantiates an HypermeaService object and starts it (with SIGTERM for docker stop).                                                                                                                                                                                |
| settings.py                     | Where you set the values of Eve [global configuration](https://docs.python-eve.org/en/stable/config.html#global-configuration) settings.  Key values are provided by `configuration/__init__.py` which are overridable by environment variables (or by `_env.conf`) |
| _env.conf                       | Set temporary/dev values for settings here.  Will not be added to container build.  If not using containers, be sure not to copy this to production.                                                                                                                |
| logging.yml                     | Configuration of the Python logging module.                                                                                                                                                                                                                         |
| requirements.txt                | Standard file for listing python libraries/dependencies - install with `pip install -r requirements.txt` .                                                                                                                                                          |
| win_service.py                  | *under development* - Lets you deploy the API as a windows service.                                                                                                                                                                                                 |
| **configuration**               |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; \_\_init\_\_.py    | Settings used by the application (some set default Eve values in `settings.py` .                                                                                                                                                                                    |
| **domain**                      | Where your domain resources will be created when you use `hypermea resource create` .                                                                                                                                                                               |
| &nbsp;&nbsp; _common.py         | Fields applied to all resources (skipped if API was created with `--no_common` ).                                                                                                                                                                                   |
| &nbsp;&nbsp; _settings.py       | Defines the `/_settings` endpoint, which you GET to see the application settings.                                                                                                                                                                                   |
| &nbsp;&nbsp; \_\_init\_\_.py    | Wires up all resources and makes them available to `HypermeaService` .                                                                                                                                                                                              |
| **hooks**                       | Wires up [Eve event hooks](https://docs.python-eve.org/en/stable/features.html#eventhooks) for logging, relationship navigation, etc.                                                                                                                               |
| &nbsp;&nbsp; _error_handlers.py |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; _logs.py           |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; _settings.py       |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; \_\_init\_\_.py    | Add your custom hooks/routes here.                                                                                                                                                                                                                                  |
| **validation**                  | This module is added when you run `add-validation` .                                                                                                                                                                                                                |
| &nbsp;&nbsp; validator.py       | Add custom validators and/or types to the `CustomHypermeaValidator` class defined here.                                                                                                                                                                             |
| **auth**                        | This module is added when you run `add-auth` (see docs for customization details).                                                                                                                                                                                  |
| &nbsp;&nbsp; auth_handlers.py   | Where you add/modify authentication handlers, (e.g. if you wish to support Digest or custom auth scheme).                                                                                                                                                           |
| &nbsp;&nbsp; authorization.py   | Defines `HypermeaAuthorization` which provides authentication to `HypermeaService` .                                                                                                                                                                                |
| &nbsp;&nbsp; \_\_init\_\_.py    | Defines the settings used by the `auth` module.                                                                                                                                                                                                                     |
| **templates**                   | This folder is added when you run `add-websocket`.                                                                                                                                                                                                                  |
| &nbsp;&nbsp; ws.html            | Contains Javascript clients use to connect to the web socket.                                                                                                                                                                                                       |
| &nbsp;&nbsp; chat.html          | An ultra simple client you can use to test the web socket.  You should delete after testing.                                                                                                                                                                        |
| **websocket**                   | This module is added when you run `add-websocket`.                                                                                                                                                                                                                  |
| &nbsp;&nbsp; \_\_init\_\_.py    | This is where you can add web socket event handlers and/or send/emit methods to broadcast onto the socket.  It currently has 'hello world' code, including the chat application (see /templates).  You should remove these as you see fit.                          |
