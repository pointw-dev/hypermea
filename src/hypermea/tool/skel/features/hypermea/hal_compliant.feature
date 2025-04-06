Feature: Resources are represented as application/hal+json

  Background:
    Given a parent and a child resource are configured
    And each resource has multiple items
    And the client requests the home resource

  Scenario: Request a parent collection resource from the home resource
    When a client requests the people resource collection
    Then its _links property includes
      | rel    | expected_href                               | is_templated |
      | self   | /people                                     | false        |
      | item   | /people/{id}                                | true         |
      | search | /people{?where,sort,max_results,page,embed} | true         |
    And the following _links do not appear
      | rel     |
      | related |
      | child   |
    And its _embedded property includes
      | rel    | type       | count |
      | people | collection | 5     |
    And each _embedded people has a _links property with
      | rel        | expected_href          | is_templated |
      | self       | /people/[[my_id]]      | false        |
      | parent     | /people                | false        |
      | collection | /people                | false        |
      | cars       | /people/[[my_id]]/cars | false        |
    And each _embedded people _links property does not include
      | rel     |
      | related |
      | child   |


  Scenario: Request a parent resource item
    When a client requests a single people resource
    Then its _links property includes
      | rel        | expected_href          | is_templated |
      | self       | /people/[[my_id]]      | false        |
      | parent     | /people                | false        |
      | collection | /people                | false        |
      | cars       | /people/[[my_id]]/cars | false        |
    And the following _links do not appear
      | rel     |
      | related |
      | child   |
    And the resource has no embedded property

  Scenario: Request a resource item's related resource collection
    When a client requests the cars belonging to one of the people collection
    Then its _links property includes
      | rel    | expected_href                                                        | is_templated |
      | self   | /people/[[first_person_id]]/cars                                     | false        |
      | parent | /people/[[first_person_id]]                                          | false        |
      | item   | /people/[[first_person_id]]/cars/{id}                                | true         |
      | search | /people/[[first_person_id]]/cars{?where,sort,max_results,page,embed} | true         |
    And the following _links do not appear
      | rel     |
      | related |
      | child   |
    And its _embedded property includes
      | rel  | type       | count |
      | cars | collection | 10    |
    And each _embedded cars has a _links property with
      | rel        | expected_href                    | is_templated |
      | self       | /cars/[[my_id]]                  | false        |
      | parent     | /people/[[first_person_id]]      | false        |
      | collection | /people/[[first_person_id]]/cars | false        |
    And each _embedded cars _links property does not include
      | rel     |
      | related |
      | child   |

  Scenario: Request a child collection resource from the home resource
    When a client requests the cars resource collection
    Then its _links property includes
      | rel    | expected_href                             | is_templated |
      | self   | /cars                                     | false        |
      | item   | /cars/{id}                                | true         |
      | search | /cars{?where,sort,max_results,page,embed} | true         |
    And the following _links do not appear
      | rel     |
      | related |
      | child   |
    And its _embedded property includes
      | rel  | type       | count |
      | cars | collection | 50    |
    And each _embedded cars has a _links property with
      | rel        | expected_href                 | is_templated |
      | self       | /cars/[[my_id]]               | false        |
      | parent     | /people/[[my_person_id]]      | false        |
      | collection | /people/[[my_person_id]]/cars | false        |
    And each _embedded cars _links property does not include
      | rel     |
      | related |
      | child   |


  Scenario: Request a child resource item
    When a client requests a single cars resource
    Then its _links property includes
      | rel        | expected_href                    | is_templated |
      | self       | /cars/[[my_id]]                  | false        |
      | parent     | /people/[[first_person_id]]      | false        |
      | collection | /people/[[first_person_id]]/cars | false        |
    And the following _links do not appear
      | rel     |
      | related |
      | child   |
    And the resource has no embedded property


  Scenario: Adding a parent item
    When a client adds a single people resource
    Then its _links property includes
      | rel        | expected_href          | is_templated |
      | self       | /people/[[my_id]]      | false        |
      | parent     | /people                | false        |
      | collection | /people                | false        |
      | cars       | /people/[[my_id]]/cars | cars         |
    And the following _links do not appear
      | rel     |
      | related |
      | child   |
    And the resource has no embedded property

  Scenario: Adding a child item
    When a client adds to the cars belonging to one of the people collection
    Then its _links property includes
      | rel        | expected_href                    | is_templated |
      | self       | /cars/[[my_id]]                  | false        |
      | parent     | /people/[[first_person_id]]      | false        |
      | collection | /people/[[first_person_id]]/cars | false        |
    And the following _links do not appear
      | rel     |
      | related |
      | child   |
    And the resource has no embedded property


  Scenario: Embedded child resources have correct links
    When a client requests a child item asking for related parent
    Then each _embedded people has a _links property with
      | rel        | expected_href          | is_templated |
      | self       | /people/[[my_id]]      | false        |
      | parent     | /people                | false        |
      | collection | /people                | false        |
      | cars       | /people/[[my_id]]/cars | false        |
    And each _embedded people _links property does not include
      | rel     |
      | related |
      | child   |

  Scenario: Embedded parent resources have correct links
    When a client requests a parent item asking for related children
    Then each _embedded cars has a _links property with
      | rel        | expected_href                 | is_templated |
      | self       | /cars/[[my_id]]               | false        |
      | parent     | /people/[[my_person_id]]      | false        |
      | collection | /people/[[my_person_id]]/cars | false        |
    And each _embedded cars _links property does not include
      | rel     |
      | related |
      | child   |
