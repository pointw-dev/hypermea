Feature: Can be debugged
  This feature is for debugging purposes only. It is not intended to be used by the end user.

  Scenario: Writes a file to the filesystem
    Given I am at a terminal
    And I am in an empty directory
    When I write a file to the filesystem
    Then the file contains the string "Hello, World!"
