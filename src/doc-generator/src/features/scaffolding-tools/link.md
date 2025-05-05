# <span class="code">link</span>

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

docs coming soon


Use `link` to manage parent/child relationships amongst resources.

## create

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

## list

details

## remove

details

