# Sorting

You can request that resource collections be sorted. Sorting is based on any field name (or field names), and can be ascending or descending.

## Request a sorted collection
### Basic
An example is worth a dozen paragraphs:

```bash
 curl -i http://localhost:2112/people?sort=city,-name
 ```

This sorts the people collection first by `city`, then by `lastname` descending.

### MongoDB style

You can also use MongoDB syntax.  That is you can use the same expression you would pass to the `.sort()` method

```bash
 curl -i http://localhost:2112/people?sort={"city":1,"name":-1}
 ```

Depending on your http library, you may need to URL encode the query string.  For example, the above `curl` command will not work unless the `{` and `}` are URL encoded:

```bash
curl -i http://localhost:2112/people?sort=%7B"city":1,"name":-1%7D
```

## Configuration
You can configure your service's sorting capability in a number of ways.

### Custom parameter name
By default, clients use `sort` in their request's query string.

If you prefer something different, change or add `QUERY_SORT` to your `settings.py` file and set it to your preference

```python
QUERY_SORT = 'order_by'
```

Now clients can use this instead of `sort`:
```bash
 curl -i http://localhost:2112/people?order_by=name
 ```


### Enable / disable sorting
By default, all requests for sorted are processed for all collections.

To globally disable this, change or add `SORTING` to your `settings.py` file and set it to `False`

```python
# settings.py
SORTING = False
```

All requests for sorting will be ignored.  You can turn them back on for individual collections in their file in the `domain/` folder.

```python{13}
# domain/people.py
SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    ...
}

DEFINITION = {
    'schema': SCHEMA,
    'sorting': True,
    'datasource': {
        'projection': {'_owner': 0}
    }
    ...
}
```

### Default sort per resource
You can set the default sort for a resource's collection.  In that resource's file in `domain/`, add/modify the `default_sort` in `datasource`.  Use MongoDB style only. 

```python{15}
# domain/people.py
SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    ...
}

DEFINITION = {
    'schema': SCHEMA,
    'datasource': {
        'projection': {'_owner': 0},
        'default_sort': {"city":1,"name":-1}
    }
    ...
}
```

### Sorting the JSON keys
In addition to sorting collections, you can also choose to sort the field keys of the JSON representation itself.  This is disabled by default.

To enable this, change or add `JSON_SORT_KEYS` to your `settings.py` file and set it to `True`

```python
# settings.py
JSON_SORT_KEYS = True
```


