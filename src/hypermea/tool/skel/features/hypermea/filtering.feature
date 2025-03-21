# https://pointw-dev.github.io/hypermea/features/runtime-capabilities/filtering.html
# https://docs.python-eve.org/en/stable/features.html#filtering

Feature: Resource collections can be filtered






    Date values should conform to RFC1123. Should you need a different format, you can change the DATE_FORMAT setting.
    - hypermea sets DATE_FORMAT to '%Y-%m-%dT%H:%M:%S' which is ISO8601

      MONGO_QUERY_BLACKLIST
      ALLOWED_FILTERS / allowed_filters
      VALIDATE_FILTERS
      QUERY_WHERE (where)
      filter [https://docs.python-eve.org/en/stable/config.html#filter]
