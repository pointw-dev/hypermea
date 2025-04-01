Feature: Resources are represented as application/hal+json

  Background:
    Given a parent and a child resource are configured
    And each resource has multiple items
    And the client has fetched the home resource

  Scenario: fetching a parent collection resource from the home resource
    When a client fetches the people resource collection
    Then its _links property includes
      | rel    | value                                       | is_templated |
      | self   | /people                                     | false        |
      | item   | /people/{id}                                | true         |
      | search | /people{?where,sort,max_results,page,embed} | true         |
    And its _embedded property includes
      | rel    | type       | count |
      | people | collection | 5     |
    And each _embedded people has a _links property with
      | rel        | value                  | is_templated |
      | self       | /people/[[my_id]]      | false        |
      | parent     | /people                | false        |
      | collection | /people                | false        |
      | cars       | /people/[[my_id]]/cars | false        |

  Scenario: fetching a parent resource item
    When a client fetches a single people resource
    Then its _links property includes
      | rel        | value                  | is_templated |
      | self       | /people/[[my_id]]      | false        |
      | parent     | /people                | false        |
      | collection | /people                | false        |
      | cars       | /people/[[my_id]]/cars | false        |
    And the resource has no embedded property

# collection links not yet implemented
  @skip
  Scenario: fetching a resource item's related resource collection
    When a client fetches the cars belonging to one of the people collection
    Then its _links property includes
      | rel    | value                                                                | is_templated |
      | self   | /people/[[first_person_id]]/cars                                     | false        |
      | parent | /people[[first_person_id]]                                           | false        |
      | item   | /cars/{id}                                                           | true         |
      | search | /people/[[first_person_id]]/cars{?where,sort,max_results,page,embed} | true         |
    And its _embedded property includes
      | rel  | type       | count |
      | cars | collection | 10    |
    And each _embedded cars has a _links property with
      | rel        | value                            | is_templated |
      | self       | /cars/[[my_id]]                  | false        |
      | parent     | /people/[[first_person_id]]      | false        |
      | collection | /people/[[first_person_id]]/cars | false        |

# something mysterious here 5/50
  @skip
  Scenario: fetching a child collection resource from the home resource
    When a client fetches the cars resource collection
    Then its _links property includes
      | rel    | value                                     | is_templated |
      | self   | /cars                                     | false        |
      | item   | /cars/{id}                                | true         |
      | search | /cars{?where,sort,max_results,page,embed} | true         |
    And its _embedded property includes
      | rel  | type       | count |
      | cars | collection | 5     |
    And each _embedded cars has a _links property with
      | rel        | value                         | is_templated |
      | self       | /cars/[[my_id]]               | false        |
      | parent     | /people/[[my_person_id]]      | false        |
      | collection | /people/[[my_person_id]]/cars | false        |


  Scenario: fetching a child resource item
    When a client fetches a single cars resource
    Then its _links property includes
      | rel        | value                            | is_templated |
      | self       | /cars/[[my_id]]                  | false        |
      | parent     | /people/[[first_person_id]]      | false        |
      | collection | /people/[[first_person_id]]/cars | false        |
    And the resource has no embedded property


  Scenario: adding a parent item
    When a client adds a single people resource
    Then its _links property includes
      | rel        | value                  | is_templated |
      | self       | /people/[[my_id]]      | false        |
      | parent     | /people                | false        |
      | collection | /people                | false        |
      | cars       | /people/[[my_id]]/cars | cars         |
    And the resource has no embedded property

  Scenario: adding a child item
    When a client adds to the cars belonging to one of the people collection
    Then its _links property includes
      | rel        | value                            | is_templated |
      | self       | /cars/[[my_id]]                  | false        |
      | parent     | /people/[[first_person_id]]      | false        |
      | collection | /people/[[first_person_id]]/cars | false        |
    And the resource has no embedded property
