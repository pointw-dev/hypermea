import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Embedding multiple resources at once')
def test_embedding_multiple_resources_at_once():
    pass

"""
Given a resource is configured having relations to two other resources
When a client requests that resource asking for each to be embedded
Then the item has both embedded resources
"""

@given('a resource is configured having relations to two other resources')
def given_a_resource_is_configured_having_relations_to_two_other_resources(dev_time_settings):
    dev_time_settings['DOMAIN'] = {
        "people": {
            "schema": {
                "name": {"type": "string"},
                "_jobs_ref": {
                    "type": "objectid",
                    "data_relation": {
                        "resource": "jobs",
                        "embeddable": True,
                        "field": "_id"
                    }
                }
            }
        },
        "jobs": {
            "schema": {
                "name": {"type": "string"},
            }
        },
        "cars": {
            "schema": {
                "name": {"type": "string"},
                "_people_ref": {
                    "type": "objectid",
                    "data_relation": {
                        "resource": "people",
                        "embeddable": True,
                        "field": "_id"
                    }
                }
            }
        },
        "people_cars": {
            "schema": {
                "name": {"type": "string"},
                "_people_ref": {
                    "type": "objectid",
                    "data_relation": {
                        "resource": "people",
                        "embeddable": True,
                        "field": "_id"
                    }
                }
            },
            "url": "people/<regex(\"[a-f0-9]{24}\"):_people_ref>/cars",
            "resource_title": "cars",
            "datasource": {
                "source": "cars"
            }
        },
        "jobs_people": {
            "schema": {
                "name": {"type": "string"},
                "_jobs_ref": {
                    "type": "objectid",
                    "data_relation": {
                        "resource": "jobs",
                        "embeddable": True,
                        "field": "_id"
                    }
                }
            },
            "url": "jobs/<regex(\"[a-f0-9]{24}\"):_jobs_ref>/people",
            "resource_title": "jobs",
            "datasource": {
                "source": "people"
            }
        }
    }


@given('the resources are populated')
def given_the_resources_are_populated(api, context):
    response = api.post('/jobs', data=json.dumps({'name':'job'}), content_type='application/json')
    assert_that(response.status_code).is_equal_to(201)
    job = response.json

    response = api.post(f'/jobs/{job["_id"]}/people', data=json.dumps({'name':'person'}), content_type='application/json')
    assert_that(response.status_code).is_equal_to(201)
    person = response.json

    cars_data = []
    for car_number in range(5):
        cars_data.append({'name': f'car {car_number + 1}'})
    response = api.post(f'/people/{person["_id"]}/cars', data=json.dumps(cars_data), content_type='application/json')
    assert_that(response.status_code).is_equal_to(201)


    context.person_id = person["_id"]


@when('a client requests that resource asking for each to be embedded')
def when_a_client_requests_that_resource_asking_for_each_to_be_embedded(api, context):
    response = api.get(f'/people/{context.person_id}?embed=jobs&embed=cars')
    assert_that(response.status_code).is_equal_to(200)
    context.resource = response.json


@then('the item has both embedded resources')
def then_the_item_has_both_embedded_resources(context):
    assert_that(context.resource).contains_key('_embedded')
    embedded = context.resource['_embedded']
    assert_that(embedded).contains_key('jobs')
    assert_that(embedded).contains_key('cars')
