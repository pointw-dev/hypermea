# hypermea
![](./img/hypermea-letterhead.svg)

## Create production-ready hypermedia APIs - *fast*

Transform your development workflow with hypermea, the toolkit that lets you rapidly create production-ready hypermedia-driven APIs. Equipped with advanced features, sophisticated error handling, expressive logging and much more, hypermea ensures your APIs are built to last, whether for small projects or enterprise-scale solutions. Discover the power of hypermedia APIs and how **hypermea makes it easy**.

> **Please note**:  We have been using hypermea internally for years to create real-life production microservice clusters. We are in the process of shrink-wrapping the package and polishing the documentation.
> This doc is under a heavy rewrite.  Information here is mostly correct, but there are gaps and it's messy.
> Version 1.0.0 is coming soon. Until its release, proceed with caution.
>
> ![](./docs/img/work-in-progress.png)


## New to hypermedia?
Hypermedia is a simple idea with powerful results.  If you are new to hypermedia, [start here](https://pointw-dev.github.io/hypermedia-docs/).

## What is hypermea?
Please see the (work in progress) [hypermea documentation](https://pointw-dev.github.io/hypermea/).

### Scaffolding tools

With simple commands you generate a fully functional, hypermedia-driven API code base in minutes. No tedious setup.

Before opening your IDE you can add resources, links, affordances. Configure authentication, Git, Docker, and more.

Start with a solid foundation and focus on what matters: your business logic.

### Runtime capabilities
Out of the box your APIs are feature rich, including sorting, pagination, filtering, validation, bulk inserts, and much more.

The APIs you create leverage <b><u><a href="https://flask.palletsprojects.com/en/stable/">Flask</a></u></b>, are powered by <b><u><a href="https://www.mongodb.com/">MongoDB</a></u></b>, and are enriched by <b><u><a href="https://docs.python-eve.org/en/stable/index.html">Eve</a></u></b>.  You get the benefits of those libraries without needing to learn them first.

With the <b><u><a href="https://pypi.org/project/hypermea-core/">hypermea-core</a></u></b> library your API is hypermedia-based using <b><u><a href="https://dev.to/nevnet99/wtf-is-hal-hypertext-application-language-2fo6">HAL</a></u></b> to represent your resources.


## Getting started

[Eve](https://docs.python-eve.org/en/stable/) is amazing.  The full power of Flask/Python, optimized for an API over mongodb.  Nice.

It does take a bit of work to go from the simple example in the docs...

```python
settings = {'DOMAIN': {'people': {}}}

app = Eve(settings=settings)
app.run()
```

...to a production-ready API, with robust exception handling, logging, control endpoints, configurability, (and so much more).

**hypermea** helps make some of that work easier.



## Command Cheat Sheet

Use the hypermea toolkit to create and craft your API.  These are command line tools, similar to how you use `git` or `docker`.

All commands begin with `hypermea` and are followed by one of the following top-level commands:

### Commands


| Command     | Definition                                                                                                                                                                                                                                                                                                                                                                                                           |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api`         | This, unsurprisingly, represents the API service itself.  When you run `hypermea api create...` a ton of code is generated, comprising your service.  The code wraps start/stop (and other details) in a class called `HypermeaService` and your app is an instance of this class.  `HypermeaService` inherits from `Flask` so your application is a Flask application as much as it is an hypermea/Eve application. |
| `resource`    | These are the 'nouns' of your service.  The set of resources you add to your API comprise the service **domain**.  Use the HTTP verbs (GET, POST, DELETE, PATCH, etc.) to operate these resources, and add affordances to enhance state management beyond CRUD.                                                                                                                                                      |
| `link`        | This creates a parent/child relationship between two resources and adds navigation affordances.                                                                                                                                                                                                                                                                                                                      |
| `affordance`  | In a Hypermedia API, clients operate your service's state by way of hyperlinks.  When you want to offer your clients the opportunity to do so, you provide a link which when requested with an HTTP verb causes the state change.  See the Hypermedia section below for more details and examples.                                                                                                                   |
| `endpoint`    | In the very unlikely event that you need to provide a capability that does not fit within the constraints of Hypermedia, you can define an arbitrary endpoint.  Use that cautiously, lest the ghost of Roy Fielding haunt you :-)                                                                                                                                                                                    |
| `docker` | When your API is equipped with `--add-docker` the `docker` command speeds up some of the mundate tasks you would do while developing and testing the API in a docker container.                                                                                                                                                                                                                                      |
| `integration` | When your service needs to use other services (whether remote or installed locally) you may find it convenient to separate the integration logic into its own module.  That what `integration` is for.  There are some built-in integrations (e.g. to AWS's S3), or you can start with a blank integration and roll your own.                                                                                        |
| `setting`     | (coming soon)                                                                                                                                                                                                                                                                                                                                                                                                        |
| `run`         | This command launches your service.  Call it anywhere in your service folder structure.                                                                                                                                                                                                                                                                                                                              |
### Help when you need it

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
