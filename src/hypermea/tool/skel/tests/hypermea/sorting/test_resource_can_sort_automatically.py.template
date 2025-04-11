import pytest
from pytest_bdd import scenario, given, when, then
from tests.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Resources can be configured to sort automatically')
def test_resource_can_sort_automatically():
    pass


@given('a resource is configured to sort automatically')
def given_a_resource_is_configured_to_sort_automatically(dev_time_settings):
    dev_time_settings['DOMAIN'] = {
        'people': {
            'schema': {
                'name': {'type': 'string'}
            },
            'datasource': {
                'default_sort': [('name', 1)]
            }
        }
    }

# And that resource has multiple items in its collection

@when('a client requests this collection without a sort query string')
def when_a_client_requests_this_collection_without_a_sort_query_string(api, context):
    response = api.get(
        '/people'
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json['_embedded']['people']

# Then the collection in the response is sorted accordingly
