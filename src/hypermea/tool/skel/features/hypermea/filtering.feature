# https://pointw-dev.github.io/hypermea/features/runtime-capabilities/search-collections/filtering.html
# https://docs.python-eve.org/en/stable/features.html#filtering

Feature: Resource collections can be filtered
    As a client
    I want to filter resource collections
    So I can fetch only those items I am interested and save bandwidth by not fetching the items I am not interested in





    Date values should conform to ISO8601. Should you need a different format, you can change the DATE_FORMAT setting.
    - e.g. DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT' # RFC1123

      MONGO_QUERY_BLACKLIST
      ALLOWED_FILTERS / allowed_filters
      VALIDATE_FILTERS
      QUERY_WHERE (where)
      filter [https://docs.python-eve.org/en/stable/config.html#filter]
