import json

from assertpy import assert_that
from pytest_bdd import given, when, parsers


@given(parsers.parse('the service is configured with a limit of {items_per_page:d} items per page'))
def given_the_service_is_configured_with_a_limit_of_items_per_page(deploy_time_settings, items_per_page):
    deploy_time_settings.hypermea.pagination_limit = items_per_page


@given('a resource is configured')
def given_a_resource_is_configured(dev_time_settings):
    dev_time_settings['DOMAIN'] = {
        'people': {
            'schema': {
                'name': {'type': 'string'}
            }
        }
    }

@given('that resource has multiple items in its collection')
def given_that_resource_has_multiple_items_in_its_collection(api, context):
    people = []
    for name in ['Robert', 'James', 'Cheryl', 'Jessica', 'Cory', 'Michael', 'Catherine', 'Mark', 'Jacqueline', 'Marissa']:
        people.append({'name': name})
    response = api.post(
        '/people',
        data=json.dumps(people),
        headers={'content-type': 'application/json'}
    )
    assert_that(response.status_code).is_equal_to(201)
    context.first_person = response.json['_items'][0]


@given('a resource is configured with multiple keys')
def given_a_resource_is_configured_with_multiple_keys(dev_time_settings):
    dev_time_settings['DOMAIN'] = {
        'widgets': {
            'schema': {
                'name': {'type': 'string'},
                'chain': {'type': 'string'},
                'significance': {'type': 'string'},
                'score': {'type': 'string'}
            }
        }
    }


@given('that resource has an item in its collection')
def given_that_resource_has_an_item_in_its_collection(api, context):
    widget = {
        'name': 'value',
        'chain': 'value',
        'significance': 'value',
        'score': 'value'
    }
    response = api.post('/widgets', data=json.dumps(widget), content_type='application/json')
    assert_that(response.status_code).is_equal_to(201)
    context.widget_id = response.json['_id']

@given('a parent and a child resource are configured')
def given_a_parent_and_a_child_resource_are_configured(dev_time_settings):
    dev_time_settings['DOMAIN'] = {
        "people": {
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
        }
    }


@given('each resource has multiple items')
def given_each_resource_has_multiple_items(api, context):
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
    context.first_person_id = first_person_id
    context.first_car_id = first_car_id


@given('the client requests the home resource')
@when('the client requests the home resource')
def given_the_client_requests_the_home_resource(api, context):
    response = api.get('/')
    context.home = response.json


@when('the client does something that causes log events to occur')
def given_the_client_does_something_that_causes_log_events_to_occur(api):
    api.get('/')


@when('a client requests a child item asking for related parent')
def when_a_client_requests_a_child_item_asking_for_related_parent(api, context):
    response = api.get(f"/cars/{context.first_car_id}?embed=people")
    assert_that(response.status_code).is_equal_to(200)
    context.resource = response.json

@when('a client requests a parent item asking for related children')
def when_a_client_requests_a_parent_item_asking_for_related_children(api, context):
    response = api.get(f"/people/{context.first_person_id}?embed=cars")
    assert_that(response.status_code).is_equal_to(200)
    context.resource = response.json

