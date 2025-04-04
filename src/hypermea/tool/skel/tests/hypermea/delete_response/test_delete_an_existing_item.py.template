import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.delete_response import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Delete an existing item')
def test_delete_an_existing_item():
    pass


@when('a client deletes an item')
def when_a_client_deletes_an_item(api, context):
    headers = {
        'If-Match': context.first_person.get('_etag'),
    }
    context.response = api.delete(f'/people/{context.first_person["_id"]}', headers=headers)
