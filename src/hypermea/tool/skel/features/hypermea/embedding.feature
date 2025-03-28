# https://pointw-dev.github.io/hypermea/features/runtime-capabilities/search-collections/embed.html


@wip
Feature: Resources can be embedded, for resource collection by default, by request for related resources
  As a client
  I want to request that a resource I fetch also includes related resources
  So that I can reduce the number of network calls I need to make

  See https://datatracker.ietf.org/doc/html/draft-kelly-json-hal-11#name-example-document for an example
  of a resource collection represented in HAL as an embedded array of resources


  Scenario: Parent resource collections are embedded by default
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests the parent resource collection
    Then the collection is in the response in the embedded property with the appropriate link relation

  Scenario: Child resource collections are embedded by default
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests the children of a parent
    Then the collection is in the response in the embedded property with the appropriate link relation

  Scenario: Embedded section does not appear for parent item when not requested
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests a parent item without asking for related children
    Then the parent item has no embedded property

  Scenario: Embedded section does appear for parent item when requested
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests a parent item asking for related children
    Then the parent's children appear in embedded property

  Scenario: Embedded section does not appear for child item when not requested
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests a child item without asking for related parent
    Then the child item has no embedded property

  Scenario: Embedded section does appear for child item when requested
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests a child item asking for related parent
    Then the child's parent item appears in embedded property

  Scenario: Embedded section does not appear for parent when requesting unrelated resource
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests a parent item with an unrelated resource
    Then the parent item has no embedded property

  Scenario: Embedded section does not appear for child when requesting unrelated resource
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests a child item with an unrelated resource
    Then the child item has no embedded property

  Scenario: Embedded collection comes with pagination controls if larger than configured limit
    Given the service is configured with a limit of 5 items per page
    And a parent and a child resource are configured
    And each resource has multiple items
    When a client requests a parent item asking for related children
    Then the parent links contain page controls for the embedded child collection

  Scenario: Embedding in a collection
    Given a parent and a child resource are configured
    And each resource has multiple items
    When a client requests the parent collection asking for embedded children
    Then each item in the embedded parent collection must contain that parent's children

#  Scenario: Embedding multiple resources at once
#    When a client performs GET /cars/abc?embed=people&embed=service-history
#    Then "_embedded.people" MUST be embedded
#    And "_embedded.service-history" MUST be embedded if links exist
