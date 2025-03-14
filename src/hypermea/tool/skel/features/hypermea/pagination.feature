# https://docs.python-eve.org/en/stable/features.html#pagination

Feature: Resource collections can split into "pages" and retrieved one page at a time
    The pagination feature is enabled by default and can be disabled both globally and/or at resource level.
        Globally with `PAGINATION` setting
        Resource level with `pagination` field in the domain definition

        PAGINATION (True) / pagination
        PAGINATION_LIMIT (50) / pagination_limit
        PAGINATION_DEFAULT (25)
        OPTIMIZE_PAGINATION_FOR_SPEED (False)

    If pagination is enabled, clients specify how they want collections to be split into pages with one or
    both of these query string parameters:
      * max_results - sets how many items max can appear in a single request, this sets the "page size"
                    - if there are 100 items in a collection, setting max_results to 20 creates 5 "pages"
                    - if not specified, the max_results is considered to be set at PAGINATION_DEFAULT or
      * page        - sets which page to fetch, based on the max_results

    You can change the parameter name from `max_results` to something else with the `QUERY_MAX_RESULTS` setting.
    You can change the parameter name from `page` to something else with the `QUERY_PAGE` setting.


    query string parameter: for example...
        GET /people?sort=lastname,-netWorth
    You can also use MongoDB format, for example...
        GET /people?sort=[("lastname", -1)]

    _meta [https://www.w3.org/TR/2011/WD-html5-20110405/links.html#sequential-link-types]
      next: 4.12.4.16.1
      prev: 4.12.4.16.2

    OPTIMIZE_PAGINATION_FOR_SPEED


