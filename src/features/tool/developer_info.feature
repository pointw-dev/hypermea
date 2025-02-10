Feature: Provides information to the developer about the tool

    The types of information a developer will want to know is the version number of the library
    and tool set installed, the commands available (usage information), and help on using those commands.


    Scenario:  View the version numbers
        Given I am at a terminal
        When I request the hypermea version
        Then the console displays the version number for both core and tool


    Scenario: View the usage information
        Given I am at a terminal
        When I run hypermea with no parameters
        Then the console displays usage information

    Scenario Outline: Get help for commands
        Given I am at a terminal
        When I request help for the <command> command
        Then the console displays help information for that <command>

        Examples:
        | command            |
        | affordance         |
        | affordance create  |
        | affordance list    |
        | affordance remove  |
        | affordance attach  |
        | api                |
        | api create         |
        | api addin          |
        | api version        |
        | docker             |
        | docker build       |
        | docker list        |
        | docker wipe        |
        | docker start       |
        | docker stop        |
        | docker up          |
        | docker down        |
        | docker cycle       |
        | docker logs        |
        | endpoint           |
        | endpoint create    |
        | endpoint list      |
        | endpoint remove    | 
        | integration        |
        | integration create |
        | integration list   |
        | link               |
        | link create        |
        | link list          |
        | link remove        |
        | resource           |
        | resource create    |
        | resource list      |
        | resource remove    |
        | resource check     |
        | run                |
        | setting            |
        | setting create     |
        | setting list       |
        | setting remove     |
