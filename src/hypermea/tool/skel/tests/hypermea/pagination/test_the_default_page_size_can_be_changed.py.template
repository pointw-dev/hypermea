import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'The default page size can be changed')
def test_the_default_page_size_can_be_changed():
    pass

@given(parsers.parse('the service is configured with a default page size of {page_size:d}'))
def given_the_service_is_configured_with_a_default_page_size_of_100(deploy_time_settings, page_size):
    deploy_time_settings.hypermea.pagination_default = page_size
