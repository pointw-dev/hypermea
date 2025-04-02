Feature: Successful deletion of collection or items provides meaningful details and links


  Background:
    Given a resource is configured
    And that resource has multiple items in its collection

  Scenario: Delete an existing item
    When a client deletes an item
    Then the response status code is 200
    And the response body has a delete count of 1
    And the response body has links with the following
      | rel  |
      | self |
      | home |


  Scenario: Delete a non-existing item
    When a client tries to delete an item that does not exist
    Then the response status code is 404
    And the response body has links with the following
      | rel  |
      | self |

  Scenario: Delete all items
    When a client deletes all items in a resource collection
    Then the response status code is 200
    And the response body has a delete count of 10
    And the response body has links with the following
      | rel  |
      | self |
      | home |


  Scenario: Delete all items twice
    When a client deletes all items in a resource collection
    And a client deletes all items in a resource collection
    Then the response status code is 200
    And the response body has a delete count of 0
    And the response body has links with the following
      | rel  |
      | self |
      | home |
