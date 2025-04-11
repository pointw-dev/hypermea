import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Pagination can be enabled per resource')
def test_pagination_can_be_enabled_per_resource():
    pass


# Given pagination is disabled globally
@given('a resource is configured to allow pagination')
def given_a_resource_is_configured_to_allow_pagination(dev_time_settings):
    dev_time_settings['DOMAIN'] = {
        'people': {
            'schema': {
                'name': {'type': 'string'}
            },
            'pagination': True
        }
    }
# And that resource has 100 items in its collection
# When a client requests this collection with a limit of <limit>
# Then the collection in the response has <limit> items
# And the prev link relation is <prev_link>
# And the next link relation is <next_link>
# And the value of the last page is <last_page>
