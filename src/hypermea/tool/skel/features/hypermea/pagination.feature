# https://pointw-dev.github.io/hypermea/features/runtime-capabilities/pagination.html
# https://docs.python-eve.org/en/stable/features.html#pagination

Feature: Resource collections can split into "pages" and retrieved one page at a time
    As a client application
    I want to be able to split collections of resources into "pages" of a certain size
      and turn the pages forwards and backwards
      and jump to the first and last page
      and jump to any arbitrary page
    So that I do not have to download an entire collection and yet still have access to all resources


    The pagination feature is enabled by default and can be disabled both globally and/or at resource level.
        Globally with `PAGINATION` setting
        Resource level with `pagination` field in the domain definition

        PAGINATION (True) / pagination
        PAGINATION_LIMIT (50/HY: 3000) / pagination_limit
        PAGINATION_DEFAULT (25/HY: 1000)
        OPTIMIZE_PAGINATION_FOR_SPEED (False)

    If pagination is enabled, clients specify how they want collections to be split into pages with one or
    both of these query string parameters:
      * max_results - sets how many items max can appear in a single request, this sets the "page size"
                    - if there are 100 items in a collection, setting max_results to 20 creates 5 "pages"
                    - if not specified, the max_results is considered to be set at PAGINATION_DEFAULT or
      * page        - sets which page to fetch, based on the max_results

    You can change the parameter name from `max_results` to something else with the `QUERY_MAX_RESULTS` setting.
    You can change the parameter name from `page` to something else with the `QUERY_PAGE` setting.

    _meta [https://www.w3.org/TR/2011/WD-html5-20110405/links.html#sequential-link-types]
      next: 4.12.4.16.1
      prev: 4.12.4.16.2


    Scenario Outline: Client can limit the number of items in a collection
        Given a resource is configured
        And that resource has 100 items in its collection
        When a client requests this collection with a limit of <limit>
        Then the collection in the response has <limit> items
        And the prev link relation is <prev_link>
        And the next link relation is <next_link>
        And the value of the last page is <last_page>

      Examples:
        | limit | next_link | prev_link | last_page |
        | 20    | present   | absent    | 5         |
        | 50    | present   | absent    | 2         |
        | 105   | absent    | absent    | absent    |

  Scenario Outline: Client can request a page in a limited collection
        Given a resource is configured
        And that resource has 100 items in its collection
        When a client requests page 2 of this collection with a limit of <limit>
        Then the collection in the response has <limit> items
        And the prev link relation is <prev_link>
        And the next link relation is <next_link>
        And the value of the last page is <last_page>

      Examples:
        | limit | next_link | prev_link | last_page |
        | 20    | present   | present   | 5         |
        | 50    | absent    | present   | absent    |
        | 105   | absent    | present   | absent    |
#         should the prev link be there in case 105?


  Scenario: Service can be configured with a different limit query string parameter
        Given the service is configured with a different limit query string parameter
        And a resource is configured
        And that resource has 100 items in its collection
        When a client requests this collection using the new limit parameter
        Then the collection in the response is limited accordingly

  Scenario: Service can be configured with a different page query string parameter
        Given the service is configured with a different page query string parameter
        And a resource is configured
        And that resource has 100 items in its collection
        When a client requests this collection using the new page parameter
        Then the collection in the response contains the correct page

  Scenario: Pagination can be disabled globally
        Given pagination is disabled globally
        And a resource is configured
        And that resource has 100 items in its collection
        When a client requests this collection with a limit of 5
        Then the limit part of the request is ignored

  Scenario Outline: Pagination can be enabled per resource
        Given pagination is disabled globally
        And a resource is configured to allow pagination
        And that resource has 100 items in its collection
        When a client requests this collection with a limit of <limit>
        Then the collection in the response has <limit> items
        And the prev link relation is <prev_link>
        And the next link relation is <next_link>
        And the value of the last page is <last_page>

      Examples:
        | limit | next_link | prev_link | last_page |
        | 20    | present   | absent    | 5         |
        | 50    | present   | absent    | 2         |
        | 105   | absent    | absent    | absent    |

  @wip
  Scenario: PAGINATION_LIMIT (50/HY: 3000)

  @wip
  Scenario:  pagination_limit

  @wip
  Scenario: PAGINATION_DEFAULT (25/HY: 1000)

  @wip
  Scenario: OPTIMIZE_PAGINATION_FOR_SPEED (False/HY: True)
