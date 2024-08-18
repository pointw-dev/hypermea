Feature: Provides information to the developer about the tool

    Scenario:  View the version numbers
        Given I am at a terminal
        When I request the hypermea version
        Then the console displays the version number for both core and tool
