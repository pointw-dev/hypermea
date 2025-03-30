from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from pytest_bdd import given, when, then, parsers
from __tests__ import *
from __tests__.hypermea import *

FEATURE_PATH = 'hypermea/embedding.feature'

"""
  Background:
    Given a parent and a child resource are configured
    And each resource has multiple items
"""


@given('a parent and a child resource are configured')
def step_impl(settings_py):
    settings_py['DOMAIN'] = {
        "people": {
            "schema": {
                "name": {"type": "string"},
            },
            'link_relation': 'person'
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
            },
            'link_relation': 'car'
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
        }
    }


@given('each resource has multiple items')
def step_impl(api, context):
    people = []
    for person_index in range(5):
        person = {
            'name': f'Person {person_index + 1}',
            'cars': []
        }
        for car_index in range(10):
            person['cars'].append({
                'name': f"Person #{person_index + 1}'s car",
            })
        people.append(person)

    first_person_id = None
    first_car_id = None
    for person in people:
        response = api.post(
            '/people',
            data=json.dumps({'name': person['name']}),
            headers={'Content-Type': 'application/json'}
        )
        assert_that(response.status_code).is_equal_to(201)
        person_id = response.json.get('_id')
        if first_person_id is None:
            first_person_id = person_id
        for car in person['cars']:
            response = api.post(
                f'/people/{person_id}/cars',
                data=json.dumps({'name': car['name']}),
                headers={'Content-Type': 'application/json'}
            )
            assert_that(response.status_code).is_equal_to(201)
            if first_car_id is None:
                first_car_id = response.json.get('_id')
    assert_that(first_person_id).is_not_none()
    assert_that(first_car_id).is_not_none()
    context['first_person_id'] = first_person_id
    context['first_car_id'] = first_car_id


@when('a client requests a parent item asking for related children')
def step_impl(api, context):
    result = api.get(f"/people/{context['first_person_id']}?embed=car")
    assert_that(result.status_code).is_equal_to(200)
    context['person'] = result.json


@then('the parent item has no embedded property')
def step_impl(context):
    assert_that(context['person']).does_not_contain('_embedded')

@then('the child item has no embedded property')
def step_impl(context):
    assert_that(context['car']).does_not_contain('_embedded')


@then("the collection is in the response in the embedded property with the appropriate link relation")
def step_impl(context):
    assert_that(context['collection']).contains_key('_embedded')
    assert_that(context['collection']['_embedded']).contains_key(context['rel'])
    assert_that(context['collection']['_embedded'][context['rel']]).is_type_of(list)
