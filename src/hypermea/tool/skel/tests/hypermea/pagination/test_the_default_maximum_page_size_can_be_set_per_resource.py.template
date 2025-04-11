import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'The default maximum page size can be set per resource')
def test_the_default_maximum_page_size_can_be_set_per_resource():
    pass


@given(parsers.parse('a resource is configured with a maximum page size of {limit:d}'))
def given_a_resource_is_configured_with_a_maximum_page_size_of_1000(dev_time_settings, limit):
    dev_time_settings['DOMAIN'] = {
        'people': {
            'schema': {
                'name': {'type': 'string'}
            },
            'pagination_limit': limit
        }
    }
