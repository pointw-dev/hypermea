# https://pointw-dev.github.io/hypermea/features/runtime-capabilities/sorting.html
# https://docs.python-eve.org/en/stable/features.html#sorting

Feature: Resource collections can be retrieved in sorted order
    As a client of the service
    I want the ability to ask that collections of resources I fetch be sorted
    So that I don't have to, and can just display or work with the sorted collection when I need it

    The sorting feature is enabled by default and can be disabled both globally and/or at resource level.
        Globally with `SORTING` setting (defaults to True)
        Resource level with `sorting` field in the domain definition

        SORTING (True) / sorting
        QUERY_SORT (sort)
        default_sort
        JSON_SORT_KEYS

    If sorting is enabled, clients specify how they want collections to be sorted with the `sort`
    query string parameter: for example...
        GET /people?sort=lastname,-netWorth
    You can also use MongoDB format, for example...
        GET /people?sort=[("lastname", -1)]

    You can change the parameter name from `sort` to something else with the `QUERY_SORT` setting.

    You can set the default sort for a resource/collection by adding `default_sort` to a domain 
    definition's `datasource` field and setting its value in MongoDB format.

    Finally (though not related to sorting collections), you can sort the keys of an individual item
    by enabling JSON_SORT_KEYS


    Scenario: Client can sort collections using the sort query string parameter
        Given a resource is configured
        And that resource has multiple items in its collection
        When a client requests this collection with a sort query string
        Then the collection in the response is sorted accordingly

    Scenario: Service can be configured with a different sort query string parameter
        Given the service is configured with a different sort query string parameter
        And a resource is configured
        And that resource has multiple items in its collection
        When a client requests this collection using the new sort parameter
        Then the collection in the response is sorted accordingly

    Scenario: Sorting can be disabled globally
        Given sorting is disabled globally
        And a resource is configured
        And that resource has multiple items in its collection
        When a client requests this collection with a sort query string
        Then the collection in the response is not sorted

    Scenario: Sorting can be specified per resource
        Given sorting is disabled globally
        And a resource is configured to allow sorting collection exists
        And that resource has multiple items in its collection
        When a client requests this collection with a sort query string
        Then the collection in the response is sorted accordingly

    Scenario: Resources can be configured to sort automatically
        Given a resource is configured to sort automatically
        And that resource has multiple items in its collection
        When a client requests this collection without a sort query string
        Then the collection in the response is sorted accordingly

    Scenario: An item's keys can be sorted
        Given key sorting is enabled
        And a resource is configured with multiple keys
        And that resource has an item in its collection
        When a client requests that resource
        Then the keys are sorted in the response
