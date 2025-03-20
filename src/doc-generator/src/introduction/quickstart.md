# Getting Started

## Install hypermea
Install hypermea into your Python virtual environment:

```bash
pip install hypermea
```

## Help when you need it
Use the hypermea toolkit to create and craft your API.  These are command line tools, similar to how you use `git` or `docker`.

All commands begin with `hypermea`.

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
What follows is a scripted walkthrough, where we will implement the following resource model step-by-step:

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
When you're satisfied, create a temporary MongoDB instance:

```bash
docker run --rm -d -p 27017:27017 --name temp-mongo mongo
```

Then run your newly minted service:

```bash
hy run
```

The first time you run this way, hypermea installs the python dependencies listed `requirements.txt` (hence the virtual environment recommendation).

### Kick the tires
The default port is 2112.  The following are some `curl` commands to explore the running service.  (or better, use [Postman](https://pointw-dev.github.io/hypermedia-docs/introduction/hypermedia-in-action/v1/explore-with-postman.html#configure-postman))

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
Now all that remains is to open the project in your IDE, add details to the domain (add fields, validations, etc.), build in your business logic, and you're off...

This just scratches the surface of how you can use **hypermea** to make your life easier.  Read on to learn more.
