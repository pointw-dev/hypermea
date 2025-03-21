# https://pointw-dev.github.io/hypermea/features/runtime-capabilities/pretty-printing.html
# https://docs.python-eve.org/en/stable/features.html#pretty-printing

Feature: Resource representations can be pretty-printed
    As a developer
    I want to to be able to request JSON responses to be in pretty-print form (i.e. indented)
    So that they are easier for me to read

    By default the JSON emitted for a resource is compact.  If you wish, you can
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
