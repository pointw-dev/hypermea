# Scaffolding tools

You use the hypermea toolkit to create and craft your API.  These are command line tools, similar to how you use git or docker.


## Top level commands
All commands begin with `hypermea` and are followed by one of the following top-level commands:

| command     | Definition                                                                                                                                                                                                                                                                                                                                                                                                           |
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

## A quick introduction
<centered-image src="/img/event-buddy-domain.svg" rounded width="450">The Event Buddy domain model</centered-image>

### Prepare the project folder
As we would with any python project, set's start with an empty folder and a python virtual environment.

```bash
mkdir event-buddy
cd event-buddy
# [recommended] create a Python virtual environment here
````

### Scaffold the model
To implement this resource model in a single service named **event-buddy**, you would execute the following commands:

```bash
hy api create event-buddy
# alternately:   hy api create .   which uses the folder name as the project name
hy resource create venues
hy resource create events
hy resource create registrations
hy resource create accounts

hy link create venues events
hy link create events registrations
hy link create accounts registrations 
```

### Verify it
You can confirm the basic scaffolding with `hy link list`

```bash
hy link list
```

which outputs

```plaintext
venues
- have events
events
- belong to a venue
- have registrations
registrations
- belong to an event
- belong to an account
accounts
- have registrations
```

In fact, if you use [PlantUML](https://editor.plantuml.com/) you can recreate the diagram above:

```bash
hy link list --format plant_uml
```

which outputs

```plaintext
@startuml
hide <<resource>> circle
hide <<remote>> circle
hide members 

skinparam class {
    BackgroundColor<<remote>> LightBlue
}

class venues <<resource>>
class events <<resource>>
class registrations <<resource>>
class accounts <<resource>>

venues ||--o{ events
events ||--o{ registrations
accounts ||--o{ registrations
@enduml
```

which you can copy/paste into the PlantUML tool of choice (e.g. the [online editor](https://editor.plantuml.com/))

### Spin it up
When you're satisfied, create a temporary mongodb instance:

```bash
docker run --rm -d -p 27017:27017 --name temp-mongo mongo
```

Then run your newly minted service:

```bash
hy run
```

The first time you run this way, hypermea installs the python dependencies listed in your projects `requirements.txt` (hence why the python virtual environment is recommended).

### Kick the tires
The default port is 2112.  The following are some curl commands to explore the running service.  (or better, use [Postman](https://pointw-dev.github.io/hypermedia-docs/introduction/hypermedia-in-action/v1/explore-with-postman.html#configure-postman))

```bash
curl http://localhost:2112 
```

or better

```bash
curl http://localhost:2112?pretty
```

dive deeper:

```bash
curl http://localhost:2112/venues?pretty
```
There are no venues yet (`"_items': []`).  Let's add one.  By default all resources have `name` and `description` fields (which you can add/remove/customize as you see fit!)

```bash
curl -X POST -u root:password localhost:2112/venues -H "Content-type: application/json" -d "{\"name\":\"Boardroom\"}"
```

And now let's look at our new venue:

```bash
curl http://localhost:2112/venues?pretty
```
How easy was that?

### Shut it down
When you're finished `Ctrl+C` on the running service to close it, then stop the mongo instance with

```bash
docker stop temp-mongo
```


## In conclusion
Now all that remains is to open the project in your IDE, flesh out the domain (add fields, validations, etc.), build in your business logic, and you're off...

This just scratches the surface of how you can use **hypermea** to make your life easier.  Read on to learn more.
