# Pretty Printing

By default, all JSON formatted resources are returned in its compact form.  This is, of course, to reduce the payload size.

It is inconvenient, though, if you want to use a tool like `curl` to fetch a resource.  Compact JSON is hard to read.

To have your service send formatted JSON instead, add the `pretty` query string parameter.  

```bash
curl http://localhost:2112/people?pretty
```

```json
{
    "_items": [
        {
            "_updated": "Tue, 19 Apr 2016 08:19:00 GMT",
            "firstname": "John",
            "lastname": "Doe",
            "born": "Thu, 27 Aug 1970 14:37:13 GMT",
            "role": [
                "author"
            ],
            "location": {
                "city": "Auburn",
                "address": "422 South Gay Street"
            },
            "_links": {
                "self": {
                    "href": "people/5715e9f438345b3510d27eb8"
                }
            },
            "_created": "Tue, 19 Apr 2016 08:19:00 GMT",
            "_id": "5715e9f438345b3510d27eb8",
            "_etag": "86dc6b45fe7e2f41f1ca53a0e8fda81224229799"
        },
        ...
    ]
}
```

You can combine this with other query string parameters, as you would with any of them, by joining multiple query string parameters with `&`

```bash
curl http://localhost:2112/people?max_results=50&pretty
```
