# https://docs.python-eve.org/en/stable/features.html#pretty-printing

Feature: Resource representations can be pretty-printed
    By default the JSON emitted by a resource is compact.  If the client wishes, it can
    receive that JSON in a "pretty" fashion, i.e. with newlines and indents

    Scenario: Client can request a pretty-printed resource
        Given a resource is configured with multiple keys
        And that resource has an item in its collection
        When a client requests that resource with pretty printing
        Then the response is pretty-printed

    Scenario: Client requests a resource without pretty-printing
        Given a resource is configured with multiple keys
        And that resource has an item in its collection
        When a client requests that resource without pretty printing
        Then the response is not pretty-printed
