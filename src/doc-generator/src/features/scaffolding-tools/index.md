---
layout: doc

prev:
  text: 'Features'
  link: '/features/'

next:
  text: '<span class="command">api</span>'
  link: '/features/scaffolding-tools/api'
---
# Scaffolding tools

## Top level commands
Use the hypermea toolkit to create and craft your API.  These are command line tools, similar to how you use `git` or `docker`.

All commands begin with `hypermea` and are followed by one of the following top-level commands:

| command                      | Definition                                                                                                                                                                                                                                                                                                                                                                                                           |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`api`](api)                 | This, unsurprisingly, represents the API service itself.  When you run `hypermea api create...` a ton of code is generated, comprising your service.  The code wraps start/stop (and other details) in a class called `HypermeaService` and your app is an instance of this class.  `HypermeaService` inherits from `Flask` so your application is a Flask application as much as it is an hypermea/Eve application. |
| [`resource`](resource)       | These are the 'nouns' of your service.  The set of resources you add to your API comprise the service **domain**.  Use the HTTP verbs (GET, POST, DELETE, PATCH, etc.) to operate these resources, and add affordances to enhance state management beyond CRUD.                                                                                                                                                      |
| [`link`](link)               | This creates a parent/child relationship between two resources and adds navigation affordances.                                                                                                                                                                                                                                                                                                                      |
| [`affordance`](affordance)   | In a Hypermedia API, clients operate your service's state by way of hyperlinks.  When you want to offer your clients the opportunity to do so, you provide a link which when requested with an HTTP verb causes the state change.  See the Hypermedia section below for more details and examples.                                                                                                                   |
| [`endpoint`](endpoint)       | In the very unlikely event that you need to provide a capability that does not fit within the constraints of Hypermedia, you can define an arbitrary endpoint.  Use that cautiously, lest the ghost of Roy Fielding haunt you :-)                                                                                                                                                                                    |
| [`docker`](docker)           | When your API is equipped with `--add-docker` the `docker` command speeds up some of the mundate tasks you would do while developing and testing the API in a docker container.                                                                                                                                                                                                                                      |
| [`integration`](integration) | When your service needs to use other services (whether remote or installed locally) you may find it convenient to separate the integration logic into its own module.  That what `integration` is for.  There are some built-in integrations (e.g. to AWS's S3), or you can start with a blank integration and roll your own.                                                                                        |
| [`setting`](setting)         | (coming soon)                                                                                                                                                                                                                                                                                                                                                                                                        |
| [`run`](run)                 | This command launches your service.  Call it anywhere in your service folder structure.                                                                                                                                                                                                                                                                                                                              |

Commands may have their own have unique sub-commands.  Many share the following:

* `create` - create the thing you're talking about, 
  * e.g. `hy api create...` or `hy resource create...`
* `list` - show the things you previously created
* `remove` - removes the thing you previously created.


## Help when you need it

You can view the above list by running `hypermea` with `--help`

```bash
hypermea --help
```

With each command, add `--help` to see more details about that command

::: tip Tip
The `hypermea` command is aliased to the shorter `hy` and you can use either interchangeably
:::

```bash
hypermea api --help
hy api create --help
```
