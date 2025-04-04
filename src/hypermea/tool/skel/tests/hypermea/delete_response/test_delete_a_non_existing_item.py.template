import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.delete_response import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Delete a non-existing item')
def test_delete_a_non_existing_item():
    pass


@when('a client tries to delete an item that does not exist')
def when_a_client_tries_to_delete_an_item_that_does_not_exist(api, context):
    context.response = api.delete(f'/people/0000')
