# hypermea
**The fastest way to build production-ready Hypermedia APIs.**



![](https://github.com/pointw-dev/hypermea/blob/main/img/hypermea-letterhead.png?raw=True)



> **Please note**:  although we currently use this toolkit to create production-ready APIs, the toolkit is still under development.  Use at your own risk.  This doc is under a heavy rewrite.  Information here is mostly correct, but there are gaps and it's messy.



## Introduction

[Eve](https://docs.python-eve.org/en/stable/) is amazing.  The full power of Flask/Python, optimized for an API over mongodb.  Nice.

It does take a bit of work to go from the simple example in the docs...

```python
settings = {'DOMAIN': {'people': {}}}

app = Eve(settings=settings)
app.run()
```

...to a production-ready API, with robust exception handling, logging, control endpoints, configurability, (and so much more).

**hypermea** helps make some of that work easier.

Install hypermea with pip.

`pip install hypermea`



## Getting Started

> This guide focusses on using the hypermea command line.  For details on methods you can use in your code, please see [hypermea-core](https://github.com/pointw-dev/hypermea-core)

All utilities are accessed through the `hypermea` command.  You can also use `hy` for short.

### Get help

To see what you can do these ools:

`hypermea --help`

or

`hy --help`

As the length of your commands grow, at each step you can always add `--help` at the end to see your options.  It is always safe to tack on a  `--help` as it only shows the help text - the command itself is not executed.

### Quick start

> NOTE: this 1-2-3 quick start assumes you have a mongodb instance running at localhost.  If you have docker installed, you can do this quickly with
>
>  `docker run --rm -d -p 27017:27017 --name my-mongo mongo`
>
> when you are done, clean up with
>
> `docker stop my-mongo`

Get started with three easy steps

1. Create your API (I recommend creating a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) first).  In an empty folder named `my-api`

   `hypermea api create .`

   

2. Add a resource to the domain

   ```bash
   hypermea resource create people
   ```



3. Launch the API

   ```bash
   hypermea run
   ```
   



Now, kick the tires of your freshly minted service.  Try it out with the following curl command (or use Postman if you prefer)

```bash
curl http://localhost:2112
curl http://localhost:2112/_settings?pretty
curl http://localhost:2112/people  (notice _items is an empty array)
curl -X POST http://localhost:2112/people -H "Content-type: application/json" -d "{\"name\":\"Michael\"}"
curl http://localhost:2112/people  (now there is one person in the _items array)
```



Stop the service (Ctrl+C where the service is running)



## Command Cheat Sheet

Use `hypermea` to create and manage several objects that make up your API.  Below are some definitions and tips to help you develop your API service to its fullest.

Note:  you can see these commands listed when you type `hypermea --help`.  

### Commands

| Term        | Definition                                                   |
| ----------- | ------------------------------------------------------------ |
| api         | This, unsurprisingly, represents the API service itself.  When you run `hypermea api create...` a ton of code is generated, comprising your service.  The code wraps start/stop (and other details) in a class called `HypermeaService` and your app is an instance of this class.  `HypermeaService` inherits from `Flask` so your application is a Flask application as much as it is an hypermea/Eve application. |
| resource    | These are the 'nouns' of your service.  The set of resources you add to your API comprise the service **domain**.  Use the HTTP verbs (GET, POST, DELETE, PATCH, etc.) to operate these resources, and add affordances to enchance state management beyond CRUD. |
| link        | This creates a parent/child relationship between two resources and adds navigation affordances. |
| affordance  | In a Hypermedia API, clients operate your service's state by way of hyperlinks.  When you want to offer your clients the opportunity to do so, you provide a link which when requested with an HTTP verb causes the state change.  See the Hypermedia section below for more details and examples. |
| endpoint    | In the very unlikely event that you need to provide a capability that does not fit within the constraints of Hypermedia, you can define an arbitrary endpoint.  Use that cautiously, lest the ghost of Roy Fielding haunt you :-) |
| integration | When your service needs to use other services (whether remote or installed locally) you may find it convenient to separate the integration logic into its own module.  That what `integration` is for.  There are some built-in integrations (e.g. to AWS's S3), or you can start with a blank integration and roll your own. |
| setting     | (coming soon)                                                |
| run         | This command launches your service.  Call it anywhere in your service folder structure. |

### Sub-commands

Most of the commands above require a sub-command.  For example,  to use `hypermea api ...`  you need to say what you want to do with the api.

To see what sub-commands and options are available:

`hypermea command --help`

e.g.,

`hypermea api --help`

Some commands have unique sub-commands, but many share the following:

* **create** - create the thing you're talking about, e.g. `hypermea api create...` or `hypermea resource create...`
* **list** - show the things you previously created
* **remove** - removes the thing you previously created.  *Note - most commands have not yet implemented `remove`*



## Command Details

### api

There are two commands that run against `api`

#### create

Creates the API service.  This command is best run in an empty folder.  

##### Service name

The first choice you must make is the name of the service.  This is the only required parameter.

e.g.,

`hypermea api create .`  (the service name will be the name of the folder you are in)

`hypermea api create whizbang`  (the service name will be `whizbang`)

##### Add-ins

After the name, you can select from several add-ins which enhance your service.  All are optional, and you can choose as many as you wish.  You can add them at create time, or any time later.

To see the add-ins available. they are listed as Options when you type:

`hypermea api create --help`

The add-ins are:

| Add in               | Description                                                 |
|----------------------| ----------------------------------------------------------- |
| -g, --add-git        | Initialize a local git repository                           |
| -d, --add-docker     | Add Dockerfile and supporting files                         |
| -a, --add-auth       | add authorization class and supporting files                |
| -v, --add-validation | add custom validation class that you can extend             |
| -w, --add-websocket  | add web socket and supporting files                         |
| -s, --add-serverless | EXPERIMENTAL: add serverless framework and supporting files |

> NOTE: You will find more details on each add-in in the next section.

You can mix and match these add-ins, e.g.,

`hypermea api create foobar --add-docker --add-git`

This is the same as

`hypermea api create foobar -dg`

If you want all add-ins, the easiest way is:

`hypermea api create foobar -davwsg`

NOTE: when you select --add-git, it will always be added last as it performs the initial commit for you.  This way all the add-ins that are installed first will be part of the commit.

#### addin

If you didn't select an add-in when you created the API, you can always select it later with the `addin` command.

In other words...

`hypermea api create foobar --add-validation`

...is the same as...

```
hypermea api create foobar
hypermea api addin --add-validation
```

...no matter how much time passes between those two statements.

All of the add-ins were introduced in the section above.  This section provides more details:

##### --add-git

details

##### --add-docker

* Adds the following files:
  `Dockerfile``
  ``docker-compose.yml` (note: by default this file does not use a volume for mongodb, so killing the container also kills your data)
  `.docker-ignore``
  ``image-build``
  ``image-build.bat`

  ...

##### --add-auth

* Adds a folder named ``auth`` with modules to add authorization to your API (docs to come)
  * NOTE: the only supported IdP is [Auth0](https://auth0.com/) at the moment, but it will be fairly easy to manually tweak to use any OAuth2 JWT issuer. (I have used a forked [Glewlwyd](https://github.com/babelouest/glewlwyd) with very minimal changes)

##### --add-validation

* adds a folder named `validation` with a module that adds custom validator to `HypermeaService`.  Use this to extend custom validations.  It comes with two validations:

  * `unique_ignorecase` - works exactly like the built-in `unique` validator except case is ignored

  * `unique_to_parent` - set this to a string of a resource's parent (singular!).  Uniqueness will only be applied to sibling resources, i.e. the same name can be used if the resource has a different parent.

    * e.g.

      ```bash
      hypermea resource create region
      hypermea resource create store
      hypermea link create region store
      ```

      Now in `domain.store`, change the name field definition from this:

      ```python
      'name": {
        'type': 'string',
              ...
        'unique': True
      }
      ```

      to this:

      ```python
      'name": {
        'type': 'string',
              ...
        'unique_to_parent': 'region'
      }
      ```

##### --add-websocket

* Define other events/listeners, emitters/senders in `websocket/__init__.py` - feel free to remove the default stuff you see there
* There is a test client at `{{BASE_API_URL}}/_ws` (which you can remove in `websocket/__init__.py` by removing the `/_ws/chat` route)
  * This is useful to see how to configure the Javascript socket.io client to connect to the web socket now running in the API
  * It is also useful to test messages - the chat app merely re-emits what it receives

##### --add-serverless

* Adds the following files:

  `serverless.py` - instantiates, but doesn't run, the HypermeaService app object.  This object is made available to the serverless framework and is referenced in the `.yml` files

  `serverless-aws.yml`

  `serverless-azure.yml`

  `serverless-google.yml`

  `logging_no-files.yml` - copy this over the original `logging.yml` to eliminate logging to the file system (which is not available with serverless)

* Also installs serverless globally with npm, does an npm init in the root api folder, and locally installs some serverless plugins (node modules).



### resource

intro

#### create

* adds *resource-name* to the domain

* default fields are name, description

* add fields by modifying domain/*resource-name*.py - as you would any hypermea resource

* NOTE: resources in Eve are collections, so hypermea names resources as plural by convention,

  * i.e. if you enter `hy resource create dog` it will create an endpoint named **/dogs**

  * hypermea relies on the [inflect](https://pypi.org/project/inflect/) library for pluralization, which is very accurate but can make mistakes

  * If you want to specify the singular and plural names of a resource use "singular,plural" e.g.  

#### check

* shows the singular and plural forms of the resource hypermea will infer  

#### list

details

#### remove

details



### link

Use `link` to manage parent/child relationships amongst resources.

#### create

* For example:

  ```bash
  hypermea resource create person
  hypermea resource create cars
  hypermea link create person car
  ```

  * you could also have typed `hypermea link create people cars` or `hypermea link create person cars` - they all are equivalent

* If you followed the example above, you have already POSTed a person named Michael:

  `curl -X POST http://localhost:2112/people -H "Content-type: application/json" -d "{\"name\":\"Michael\"}"`

* Normally GET a person by `_id`.   **hypermea** wires up the name field as an `additonal_lookup`, so you can also GET by name.

  `curl http://localhost:2112/people/Michael?pretty`

  ```json
  {
    "_id": "606f5453b43a8f480a1b8fc6",
    "name": "Michael",
    "_updated": "2021-04-08T19:06:59",
    "_created": "2021-04-08T19:06:59",
    "_etag": "6e91d500cbb0a2f6645d9b4dced422d429a69820",
    "_links": {
      "self": { "href": "/people/606f5453b43a8f480a1b8fc6", "title": "person" },
      "parent": { "title": "home", "href": "/" },
      "collection": { "title": "people", "href": "people" },
      "cars": { "href": "/people/606f5453b43a8f480a1b8fc6/cars", "title": "cars" }
    }
  }
  ```

* Notice the `_links` field includes a rel named `cars`.  You can POST a car to that `href` (I'll demonstrate with Javascript):

  ```javascript
  const axios = require('axios')
  axios.defaults.baseURL = 'http://localhost:2112'
  
  axios.get('/people/Michael').then((response) => {
      const person = response.data
      const car = {
          name: 'Mustang'
      }
      axios.post(person._links.cars.href, car)
  })
  ```

* `-p` `--as_parent_ref`:  field name defaults to `_` *parent-resource* `_ref`, e.g. if the parent name was dogs the field would be `_dog_ref`.  Using this parameter, the field name become literally `_parent_ref`.  Useful to implement generic parent traversals.

#### list

details

#### remove

details



### affordance

intro

#### create

details

#### attach

details

#### list

details

#### remove

details



### endpoint

intro

#### create

details

#### list

details

#### remove

details



### 

### integration

intro

#### create

details

#### list

details

#### remove

details



### setting

intro

#### create

details

#### list

details

#### remove

details



### run

details



## Features

This section is under heavy construction.  In no particular order...

### Settings/configuration system

The `HypermeaService` ships with a sophisticated settings/configuration management system based on these principles:

* Easy to run: An API should run right out of the box without requiring configuration
* Container compatible: All settings can be set with environment variables.
* Developer convenience:  Developers can easily modify settings without accidentally commiting code with experimental values.
  * use `_env.conf` to set these values - included when your API was created
  * This file is in `.gitignore` and `.dockerignore` so it will never accidentally be shipped anywhere but your dev environment
* Visible:  all setting values are logged at startup and can be viewed with `GET /_settings` - no more wondering what value was set when debugging a problem at 3:00 AM

(TODO: cancellable, optional, prefix stuff?,  `settings.has_enabled()`   [0] == 'YyTtEe')

### Logging

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

### Echo

Sometimes you need to test a client's ability to respond to various message or error/status codes.  It may be difficult to purposefully generate a 500.  In these cases you can enable `HY_ADD_ECHO`.  Then you can PUT to `/_echo` a JSON as follows:

```json
{
  "status_code": ###,
  "message": {...}
}
```

This produce a response with status code as specified, with the `message` value as the body.  It also goes through the service logging system, so you can test receiving emails on 5xx, etc. (or however you choose to extend the logging)

### Exception Handling

* improves on Eve's out-of-box behaviour by standardizing the error response - even in the case of 5xx's
  `{_status: "ERR", _error: {code:422, message: ""}, _issues: [] }`
* your code can call `utils.make_error_response()` to emit custom error messages that follow this standard.

HAL media type

* Eve's out-of-box JSON structure is very close to HAL.  With hypermea, you get even closer
  * Content-type is `application/hal+json`
  * `_links` are tidied up, some superfluous metadata is removed
  * hierarchical navigation follows IANA conventions
  * (this is constantly improving - coming soon curies, _embedded, as well as other standard hypermedia types like Siren, Atom, Collection+JSON, etc.)

### API Gateway Registration

(details)

### Miscellaneous

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
