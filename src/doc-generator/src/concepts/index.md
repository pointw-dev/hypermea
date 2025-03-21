# Basic concepts

## Hypermedia
When you use hypermea to create your service, it is organized around the concept of hypermedia.  If this is new to you, please check out [this site](https://pointw-dev.github.io/hypermedia-docs) to learn more.

## Resources
When you create a resource in hypermea (e.g. `hy resource create widget`), two things happen.
* The collection of resources has an endpoint
  * `GET /widgets` fetches the collection of widgets that have been previously POSTed
* Each resource POSTed has its own endpoint
  * `GET /widgets/{id}` fetches the one widget with that `id`

Of course, when your client uses hypermedia, it will never know the URLs for these endpoints.  Both the service dev team and the client dev team needs to know each resource exists as a collection and as individual items.

When a client fetches a resource collection, the `_links` will look something like this:

```json

```
