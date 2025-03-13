Feature: Clients can request that collection resources be sorted

    Sorting is enabled by default and can be disabled both globally and/or at resource level.

    Globally with `SORTING` setting
    Resource level with `sorting` field in the domain definition

    If sorting is enabled, clients specify how they want collections to be sorted with the `sort`
    query string parameter: for example
        GET /people?sort=lastname,-netWorth
    You can also use MongoDB format, for example
        GET /people?sort=[("lastname", -1)]

    You can change the parameter name from `sort` to something else with the `QUERY_SORT` setting.

    You can set the default sort for a resource/collection by adding `default_sort` to a domain 
    definition's `datasource` field and setting its value in MongoDB format.

    Finally (though not related to sorting collections), you can sort the keys of an individual item by enabling JSON_SORT_KEYS


    Scenario: Client can sort collections using the sort query string parameter
        Given a resource collection exists
        And a resource has multiple items in its collection
        When a client requests this collection with a sort query string
        Then the collection in the response is sorted accordingly

    Scenario: Service can be configured with a different sort query string parameter
        Given the service is configured with a different sort query string parameter
        And a resource collection exists
        And a resource has multiple items in its collection
        When a client requests this collection using the new sort parameter
        Then the collection in the response is sorted accordingly

    Scenario: Sorting can be disabled globally
        Given sorting is disabled globally
        And a resource collection exists
        And a resource has multiple items in its collection
        When a client requests this collection with a sort query string
        Then the collection in the response is not sorted

    Scenario: Sorting can be specified at per resource
        Given sorting is disabled globally
        And a resource configured to sort collection exists
        And a resource has multiple items in its collection
        When a client requests this collection with a sort query string
        Then the collection in the response is sorted accordingly
