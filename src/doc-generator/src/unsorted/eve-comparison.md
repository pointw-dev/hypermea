# Eve Comparison

:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::


<style>
table.side-by-side {
  width: 875px;
  margin-left: -75px !important;
}
td.json {
  font-family: monospace;
  vertical-align: top;
}
td.large-json {
  font-size: 9pt;
  vertical-align: top;
}
td.larger-json {
  font-size: 8.5pt;
  vertical-align: top;
}
tr.header {
  font-weight: bold;
}
</style>


:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::

This page is for those coming to hypermea from eve.  Hypermea is powered by eve so many things will be familiar.  However, there are some significant departures.  



## Settings
Eve has one dict for all settings.  Hypermea groups settings into four categories

* fixed - defined and set in `settings.py`   (aka dev-time)
  * The values of these settings are set before the app is deployed and can only be changed by re-deploying.
  * All eve settings are "fixed" unless "elevated" to a hypermea base setting  
* deploy-time
  * base - these are defined by environment variables.  
    * Some eve settings have been "elevated" to a base setting (e.g. HY_PAGINATION_LIMIT sets the eve setting PAGINATION_LIMIT) with the only differences being the name, and the fact that they can be changed without a re-deploy
    * the other base settings have been added for use by all services created wtih hypermea
  * api - these are settings added to your API for purpose of the unique requirements of your service
  * integration - these settings are used to connect to anything outside your service, e.g. S3 (bucket name, credentials)
* run-time
  * logging verbosity per handler
  * (more to come?)

| Eve setting                   | Eve default           | Hypermea setting      | Hypermea default                    |
|-------------------------------|-----------------------|-----------------------|-------------------------------------|
| DATE_FORMAT                   | _RFC 1123_            | _unchanged_           | _ISO 8601_                          |
| PAGINATION_LIMIT              | `50`                  | HY_PAGINATION_LIMIT   | `3000`                              |
| PAGINATION_DEFAULT            | `25`                  | HY_PAGINATION_DEFAULT | `1000`                              |
| SCHEMA_ENDPOINT               | `None`                | _unchanged_           | `'_schema'`                         |
| RESOURCE_METHODS              | `['GET']`             | _unchanged_           | `['GET', 'POST', 'DELETE']`         |
| ITEM_METHODS                  | `['GET']`             | _unchanged_           | `['GET', 'PATCH', 'DELETE', 'PUT']` |
| AUTH_FIELD                    | `None`                | _unchanged_           | `_owner`                            | 
| MONGO_HOST                    | `localhost`           | HY_MONGO_HOST         | _unchanged_                         |
| MONGO_PORT                    | `27017`               | HY_MONGO_PORT         | _unchanged_                         |
| MONGO_DBNAME                  | 'eve'                 | HY_MONGO_DBNAME       | the value of `HY_API_NAME`          |
| MONGO_USERNAME                | `None`                | HY_MONGO_USERNAME     | _unchanged_                         |
| MONGO_PASSWORD                | `None`                | HY_MONGO_PASSWORD     | _unchanged_                         |
| MONGO_AUTHSOURCE              | `None`                | HY_MONGO_AUTHSOURCE   | _unchanged_                         |
| MONGO_QUERY_BLACKLIST         | `['$where','$regex']` | _unchanged_           | `['$where']`*                       |
| URL_PREFIX                    | `None`                | HY_URL_PREFIX         | _unchanged_                         |
| CACHE_CONTROL                 | `None`                | HY_CACHE_CONTROL      | _unchanged_                         |
| CACHE_EXPIRES                 | `None`                | HY_CACHE_EXPIRES      | _unchanged_                         |



```
| OPTIMIZE_PAGINATION_FOR_SPEED | `False`               | _unchanged_           | `True`                              |
- was set to True, now false - not only does _meta.count disappear if True, but also pagination links to 'last' page
```

(see also [CORS](#cors), [Rate Limit](#rate-limit) [Resource Representation](#resource-representation))

## CORS
By default hypermea sets the following eve settings to enable CORS
```python
X_DOMAINS = '*'
X_EXPOSE_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']
X_HEADERS = [
    'Accept',
    'Authorization',
    'If-Match',
    'Access-Control-Expose-Headers',
    'Access-Control-Allow-Origin',
    'Content-Type',
    'Pragma',
    'X-Requested-With',
    'Cache-Control'
]
```
The Flask app is also provisioned in the `HypermeaService` class  with [flask-cors](https://corydolphin.com/flask-cors/).

Hypermea uses a singleton class that is useable as a dict (so referring to settings in code will follow the same pattern)

## Rate Limit
The eve documentation on rate limiting (as of this writing) is still pending.  With Eve you must set the rate limit individually for each http method [GET, POST, PATCH, DELETE].  You can do that as well with hypermea, or you can set one limit that applies to all methods (and you can mix and match).

TODO: explain the following - or better yet, link to [Rate Limiting](/features/runtime-capabilities/rate-limiting) 
```python
SETTINGS.create('HY', 'RATE_LIMIT', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_GET', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_POST', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_PATCH', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_DELETE', is_optional=True)
```


## Vocabulary
* What eve calls "resource" and "item", hypermea prefers "resource collection" and "resource item".  This distinction is primarily in documentation and not necessarily in code.  Note that resources lend their plural names to URL paths (e.g. `/people`, `/people/123`) but link relations are named using their singular.


## The app object
A typical eve app (or any Flask app) instantiates and manipulates an app object.  Hypermea wraps the app manipulation into a class named `HypermeaService` which can be started and stopped.  This allows for a variety of run-time options, from the built-in `run.py` to serverless deployments, even as a Windows service.


## Misc
```python
eve_passthrough('MEDIA_BASE_URL')
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']
```

## Resource representation
Clients written to consume an eve based API will require changes before they will work with hypermea.  This is because eve emits its own flavour of JSON while hypermea emits HAL.

By default, the value of eve's `RENDERERS` setting is `['eve.render.JSONRenderer','eve.render.XMLRenderer]`  In hypermea this is set to `['hypermea.core.render.HALRenderer']`

### Domain Model
To see the difference, we will work with a DOMAIN with `people` and `cars`.  An item in the `people` resource is associated with any number of items in the `cars` resource - what eve calls "sub-resources".

<centered-image src="/img/people-cars.svg" rounded width="250">A simple domain model</centered-image>


<table class="side-by-side">
<thead>
<tr class="header">
<td>to create this in eve</td>
<td>to create this in hypermea</td>
</tr>
</thead>
<tbody>
<tr>

<td class="json">

```python
DOMAIN = {
  "people" : {
    "schema" : {
      "name" : {
        "type" : "string",
        "required" : True
      }
    },
  },
  "cars" : {
    "schema" : {
      "name" : {
        "type" : "string",
        "required" : True
      },
      "_people_ref" : {
        "type" : "objectid",
        "data_relation" : {
          "resource" : "people",
          "embeddable" : True,
          "field" : "_id"
        }
      }
    },
  "people_cars" : {
    "schema" : {
      "name" : {
        "type" : "string",
        "required" : true
      },
      "_people_ref" : {
        "type" : "objectid",
        "data_relation" : {
          "resource" : "people",
          "embeddable" : True,
          "field" : "_id"
        }
      }
    },
    "url" : "people/<regex(\"[a-f0-9]{24}\"):_people_ref>/cars",
    "resource_title" : "cars",
    "datasource" : {
      "source" : "cars"
      }
    }    
  }
}
```
</td>

<td class="json">

```bash
hy resource create person
hy resource create car
hy link create person car
```
</td>

</tr>
</tbody>
</table>







### home resource
<table class="side-by-side">
<thead>
<tr class="header">
<td>from eve</td>
<td>from hypermea</td>
</tr>
</thead>
<tbody>
<tr>
<td class="json">GET /</td>
<td class="json">GET /</td>
</tr>
<tr>
<td class="json">Content-Type: application/json</td>
<td class="json">Content-Type: application/hal+json</td>
</tr>
<tr>

<td class="json">

```json
{
  "_links": {
    "child": [
      {
        "href": "people",
        "title": "people"
      },
      {
        "href": "cars",
        "title": "cars"
      },
      {
        "href": "people/<_people_ref>/cars",
        "title": "cars"
      }
    ]
  }
}
```
</td>

<td class="large-json">

```json
{
  "_links": {
    "self": {
      "href": "/",
      "_note": "Home resource for dev-hypermea-api"
    },
    "logging": {
      "href": "/_logging",
      "_note": "logging verbosity: GET, PUT"
    },
    "settings": {
      "href": "/_settings",
      "_note": "versions and settings: GET"
    },
    "person": {
      "href": "/people",
      "_note": "add ?links_only query string to GET _links without the collection"
    },
    "car": {
      "href": "/cars",
      "_note": "add ?links_only query string to GET _links without the collection"
    }
  }
}
```
</td>

</tr>
</tbody>
</table>





### people resource collection
<table class="side-by-side">
<thead>
<tr class="header">
<td>from eve</td>
<td>from hypermea</td>
</tr>
</thead>
<tbody>
<tr>
<td class="json">home._links.people.href</td>
<td class="json">home._links.person.href</td>
</tr>
<tr>
<td class="json">GET /people</td>
<td class="json">GET /people</td>
</tr>
<tr>

<td class="large-json">

```json
{
    "_items": [
        {
            "_id": "67f127fbacccb8d36a514f8d",
            "name": "Pat",
            "_updated": "Sat, 05 Apr 2025 12:54:19 GMT",
            "_created": "Sat, 05 Apr 2025 12:54:19 GMT",
            "_etag": "d64ea3f9d672146e49e4babe2407eb0179074e36",
            "_links": {
                "self": {
                    "title": "People",
                    "href": "people/67f127fbacccb8d36a514f8d"
                }
            }
        },
        {
            "_id": "67f127fdacccb8d36a514f8e",
            "name": "Darcy",
            "_updated": "Sat, 05 Apr 2025 12:54:21 GMT",
            "_created": "Sat, 05 Apr 2025 12:54:21 GMT",
            "_etag": "be7b83ec1bdd641e73fc776eef7f52cda5306cb6",
            "_links": {
                "self": {
                    "title": "People",
                    "href": "people/67f127fdacccb8d36a514f8e"
                }
            }
        },
        {
            "_id": "67f127feacccb8d36a514f8f",
            "name": "Alex",
            "_updated": "Sat, 05 Apr 2025 12:54:22 GMT",
            "_created": "Sat, 05 Apr 2025 12:54:22 GMT",
            "_etag": "0ecbc60932b7a27d6002b9883ac47013676ccae9",
            "_links": {
                "self": {
                    "title": "People",
                    "href": "people/67f127feacccb8d36a514f8f"
                }
            }
        }
    ],
    "_links": {
        "parent": {
            "title": "home",
            "href": "/"
        },
        "self": {
            "title": "people",
            "href": "people"
        }
    },
    "_meta": {
        "page": 1,
        "max_results": 25,
        "total": 3
    }
}
```
</td>

<td class="larger-json">

```json
{
    "_links": {
        "parent": {
            "href": "/people"
        },
        "self": {
            "href": "/people"
        },
        "create-form": {
            "href": "people/create-form",
            "_note": "GET to fetch create-form to add to people"
        },
        "collection": {
            "href": "/people"
        },
        "item": {
            "href": "/people/{id}",
            "templated": true
        },
        "search": {
            "href": "/people{?where,sort,max_results,page,embed}",
            "templated": true
        }
    },
    "_meta": {
        "page": 1,
        "max_results": 1000,
        "total": 3
    },
    "_embedded": {
        "person": [
            {
                "_id": "67f19983642f901ff3892b50",
                "name": "Pat",
                "_updated": "2025-04-05T20:58:43",
                "_created": "2025-04-05T20:58:43",
                "_etag": "914f5daac98c95b86e9159f3a9e200969ea511f3",
                "_links": {
                    "self": {
                        "href": "/people/67f19983642f901ff3892b50"
                    },
                    "car": {
                        "href": "/people/67f19983642f901ff3892b50/cars"
                    },
                    "parent": {
                        "href": "/people"
                    },
                    "collection": {
                        "href": "/people"
                    }
                }
            },
            {
                "_id": "67f19988642f901ff3892b51",
                "name": "Darcy",
                "_updated": "2025-04-05T20:58:48",
                "_created": "2025-04-05T20:58:48",
                "_etag": "906e8349d58cbd97b2e0ae149f27290784ebbfeb",
                "_links": {
                    "self": {
                        "href": "/people/67f19988642f901ff3892b51"
                    },
                    "car": {
                        "href": "/people/67f19988642f901ff3892b51/cars"
                    },
                    "parent": {
                        "href": "/people"
                    },
                    "collection": {
                        "href": "/people"
                    }
                }
            },
            {
                "_id": "67f1998d642f901ff3892b52",
                "name": "Alex",
                "_updated": "2025-04-05T20:58:53",
                "_created": "2025-04-05T20:58:53",
                "_etag": "429b154493079fba1570e1624022fae7cb1317cd",
                "_links": {
                    "self": {
                        "href": "/people/67f1998d642f901ff3892b52"
                    },
                    "car": {
                        "href": "/people/67f1998d642f901ff3892b52/cars"
                    },
                    "parent": {
                        "href": "/people"
                    },
                    "collection": {
                        "href": "/people"
                    }
                }
            }
        ]
    }
}
```
</td>

</tr>
</tbody>
</table>






### person by id

<table class="side-by-side">
<thead>
<tr class="header">
<td>from eve</td>
<td>from hypermea</td>
</tr>
</thead>
<tbody>
<tr>
<td><i>constructed URL</i></td>
<td class="json">home.person._links.item(id)</td>
</tr>

<tr>
<td class="json">GET /people/{id}</td>
<td class="json">GET /people/{id}</td>
</tr>
<tr>

<td class="json">

```json
{
  "_id": "67f127fbacccb8d36a514f8d",
  "name": "Pat",
  "_updated": "Sat, 05 Apr 2025 12:54:19 GMT",
  "_created": "Sat, 05 Apr 2025 12:54:19 GMT",
  "_etag": "d64ea3f9d672146e49e4babe2407eb0179074e36",
  "_links": {
    "self": {
      "title": "People",
      "href": "people/67f127fbacccb8d36a514f8d"
    },
    "parent": {
      "title": "home",
      "href": "/"
    },
    "collection": {
      "title": "people",
      "href": "people"
    }
  }
}
```
</td>

<td class="json">

```json
{
  "_id": "67f19983642f901ff3892b50",
  "name": "Pat",
  "_updated": "2025-04-05T20:58:43",
  "_created": "2025-04-05T20:58:43",
  "_etag": "914f5daac98c95b86e9159f3a9e200969ea511f3",
  "_links": {
    "self": {
      "href": "/people/67f19983642f901ff3892b50"
    },
    "parent": {
      "href": "/people"
    },
    "collection": {
      "href": "/people"
    },
    "edit-form": {
      "href": "/people/67f19983642f901ff3892b50/edit-form",
      "_note": "GET to fetch edit-form"
    },
    "car": {
      "href": "/people/67f19983642f901ff3892b50/cars"
    }
  }
}
```
</td>

</tr>
</tbody>
</table>

(it is clear a `person` is related to `car`)



### car by id

<table class="side-by-side">
<thead>
<tr class="header">
<td>from eve</td>
<td>from hypermea</td>
</tr>
</thead>
<tbody>
<tr>
<td><i>constructed URL</i></td>
<td class="json">person._links.car.item(id)<br/><i>or</i> home.car.item(id)</td>
</tr>
<tr>
<td>GET /cars/{id}</td>
<td>GET /cars/{id}</td>
</tr>
<tr>

<td class="json">

```json
{
    "_id": "67f19b3f4f8891ecba5ec905",
    "name": "Ford Mustang",
    "_people_ref": "67f127fbacccb8d36a514f8d",
    "_updated": "Sat, 05 Apr 2025 21:06:07 GMT",
    "_created": "Sat, 05 Apr 2025 21:06:07 GMT",
    "_etag": "f1297e90cd1df584362956777b07ba1bef8082f3",
    "_links": {
        "self": {
            "title": "Car",
            "href": "cars/67f19b3f4f8891ecba5ec905"
        },
        "related": {
            "_people_ref": {
                "title": "People",
                "href": "people/67f127fbacccb8d36a514f8d"
            }
        },
        "parent": {
            "title": "home",
            "href": "/"
        },
        "collection": {
            "title": "cars",
            "href": "cars"
        }
    }
}
```
</td>

<td class="large-json">

```json
{
    "_id": "67f19b2c642f901ff3892b53",
    "name": "Ford Mustang",
    "_people_ref": "67f19983642f901ff3892b50",
    "_updated": "2025-04-05T21:05:48",
    "_created": "2025-04-05T21:05:48",
    "_etag": "9ff48752c7e825febe6ec090c3772b104881ea85",
    "_links": {
        "self": {
            "href": "/cars/67f19b2c642f901ff3892b53"
        },
        "parent": {
            "href": "/people/67f19983642f901ff3892b50"
        },
        "collection": {
            "href": "/people/67f19983642f901ff3892b50/cars"
        },
        "edit-form": {
            "href": "/cars/67f19b2c642f901ff3892b53/edit-form",
            "_note": "GET to fetch edit-form"
        },
        "person": {
            "href": "/people/67f19983642f901ff3892b50"
        }
    }
}
```
</td>

</tr>
</tbody>
</table>




### car, embedding person

<table class="side-by-side">
<thead>
<tr class="header">
<td>from eve</td>
<td>from hypermea</td>
</tr>
</thead>
<tbody>
<tr>
<td class="json">GET /cars/{id}?embedded={"_people_ref":1}</td>
<td class="json">GET /cars/{id}?embed=person</td>
</tr>
<tr>

<td class="large-json">

```json
{
    "_id": "67f19b3f4f8891ecba5ec905",
    "name": "Ford Mustang",
    "_people_ref": {
        "_id": "67f127fbacccb8d36a514f8d",
        "name": "Pat",
        "_updated": "Sat, 05 Apr 2025 12:54:19 GMT",
        "_created": "Sat, 05 Apr 2025 12:54:19 GMT",
        "_etag": "d64ea3f9d672146e49e4babe2407eb0179074e36"
    },
    "_updated": "Sat, 05 Apr 2025 21:06:07 GMT",
    "_created": "Sat, 05 Apr 2025 21:06:07 GMT",
    "_etag": "f1297e90cd1df584362956777b07ba1bef8082f3",
    "_links": {
        "self": {
            "title": "Car",
            "href": "cars/67f19b3f4f8891ecba5ec905"
        },
        "related": {
            "_people_ref": {
                "title": "People",
                "href": "people/67f127fbacccb8d36a514f8d"
            }
        },
        "parent": {
            "title": "home",
            "href": "/"
        },
        "collection": {
            "title": "cars",
            "href": "cars"
        }
    }
}
```
</td>

<td class="large-json">

```json
{
    "_id": "67f19b2c642f901ff3892b53",
    "name": "Ford Mustang",
    "_people_ref": "67f19983642f901ff3892b50",
    "_updated": "2025-04-05T21:05:48",
    "_created": "2025-04-05T21:05:48",
    "_etag": "9ff48752c7e825febe6ec090c3772b104881ea85",
    "_links": {
        "self": {
            "href": "/cars/67f19b2c642f901ff3892b53"
        },
        "parent": {
            "href": "/people/67f19983642f901ff3892b50"
        },
        "collection": {
            "href": "/people/67f19983642f901ff3892b50/cars"
        },
        "edit-form": {
            "href": "/cars/67f19b2c642f901ff3892b53/edit-form",
            "_note": "GET to fetch edit-form"
        },
        "person": {
            "href": "/people/67f19983642f901ff3892b50"
        }
    },
    "_embedded": {
        "person": {
            "_id": "67f19983642f901ff3892b50",
            "name": "Pat",
            "_updated": "2025-04-05T20:58:43",
            "_created": "2025-04-05T20:58:43",
            "_etag": "914f5daac98c95b86e9159f3a9e200969ea511f3",
            "_links": {
                "self": {
                    "href": "/people/67f19983642f901ff3892b50"
                },
                "parent": {
                    "href": "/people"
                },
                "collection": {
                    "href": "/people"
                },
                "edit-form": {
                    "href": "/people/67f19983642f901ff3892b50/edit-form",
                    "_note": "GET to fetch edit-form"
                },
                "car": {
                    "href": "/people/67f19983642f901ff3892b50/cars"
                }
            }
        }
    }
}
```
</td>

</tr>
</tbody>
</table>

(with hypermea you know the query string value is `person` because a car has a link to a `person`)



### person, embedding cars


<table class="side-by-side">
<thead>
<tr class="header">
<td>from eve</td>
<td>from hypermea</td>
</tr>
</thead>
<tbody>
<tr>
<td class="json">???</td>
<td class="json">GET /people/{id}?embed=car</td>
</tr>
<tr>

<td class="json">

<pre>???</pre>

</td>

<td class="json">

```json
{
    "_id": "67f19983642f901ff3892b50",
    "name": "Pat",
    "_updated": "2025-04-05T20:58:43",
    "_created": "2025-04-05T20:58:43",
    "_etag": "914f5daac98c95b86e9159f3a9e200969ea511f3",
    "_links": {
        "self": {
            "href": "/people/67f19983642f901ff3892b50"
        },
        "parent": {
            "href": "/people"
        },
        "collection": {
            "href": "/people"
        },
        "edit-form": {
            "href": "/people/67f19983642f901ff3892b50/edit-form",
            "_note": "GET to fetch edit-form"
        },
        "car": {
            "href": "/people/67f19983642f901ff3892b50/cars"
        }
    },
    "_embedded": {
        "car": [
            {
                "_id": "67f19b2c642f901ff3892b53",
                "name": "Ford Mustang",
                "_people_ref": "67f19983642f901ff3892b50",
                "_updated": "2025-04-05T21:05:48",
                "_created": "2025-04-05T21:05:48",
                "_etag": "9ff48752c7e825febe6ec090c3772b104881ea85",
                "_links": {
                    "self": {
                        "href": "/cars/67f19b2c642f901ff3892b53"
                    },
                    "person": {
                        "href": "/people/67f19983642f901ff3892b50"
                    },
                    "parent": {
                        "href": "/people/67f19983642f901ff3892b50"
                    },
                    "collection": {
                        "href": "/people/67f19983642f901ff3892b50/cars"
                    }
                }
            },
            {
                "_id": "67f19b2c642f901ff3892b54",
                "name": "Chrysler 300",
                "_people_ref": "67f19983642f901ff3892b50",
                "_updated": "2025-04-05T21:05:48",
                "_created": "2025-04-05T21:05:48",
                "_etag": "b9eb314afc8d55530c16c430d89dbe2bfad0d302",
                "_links": {
                    "self": {
                        "href": "/cars/67f19b2c642f901ff3892b54"
                    },
                    "person": {
                        "href": "/people/67f19983642f901ff3892b50"
                    },
                    "parent": {
                        "href": "/people/67f19983642f901ff3892b50"
                    },
                    "collection": {
                        "href": "/people/67f19983642f901ff3892b50/cars"
                    }
                }
            }
        ]
    }
}
```
</td>

</tr>
</tbody>
</table>


