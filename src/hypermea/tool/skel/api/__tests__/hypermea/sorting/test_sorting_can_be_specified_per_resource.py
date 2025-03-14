import pytest
from pytest_bdd import scenario, given, when, then

from __tests__.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Sorting can be specified at per resource')
def test_test_sorting_can_be_specified_per_resource():
    pass


# Given sorting is disabled globally
@given('a resource is configured to allow sorting collection exists')
def step_impl(eve_settings):
    eve_settings['DOMAIN'] = {
        'people': {
            'schema': {
                'name': {'type': 'string'}
            },
            'sorting': True
        }
    }

# And that resource has multiple items in its collection
# When a client requests this collection with a sort query string
# Then the collection in the response is sorted accordingly
