import json
import uritemplate

from tests import *
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that

FEATURE = 'hypermea/hal_compliant.feature'


def href_from_resource(resource, rel, template_values=None):
    url = resource.get('_links', {}).get(rel, {}).get('href')
    url = uritemplate.expand(url, template_values or {})
    return url

def validate_links(context, resource, datatable):
    for row in datatable[1:]:  # peel off header row
        rel, expected_href, is_templated = row
        my_id = resource.get('_id', '')
        person_ref = resource.get('_people_ref', '')
        expected_href = (expected_href
                 .replace('[[first_person_id]]', context.first_person_id)
                 .replace('[[first_car_id]]', context.first_car_id)
                 .replace('[[my_id]]', my_id)
                 .replace('[[my_person_id]]', person_ref)
                 )
        link = resource.get('_links', {}).get(rel, {})
        href = link.get('href')
        assert_that(href).is_equal_to(expected_href)
        assert_that(any(href.startswith(prefix) for prefix in ['http', '/'])).is_true()
        assert_that(link.get('templated', False)).is_equal_to(is_templated == 'true')

        # Eve inserts a "title" for a link in case the client app wants to use it as a prompt,
        # but it is almost never useful.  Hypermea removes it.
        assert_that(link.get('title', None)).is_none()

def validate_no_unacceptable_links(resource, datatable):
    for row in datatable[1:]:  # peel off header row
        rel, = row
        assert_that(resource['_links']).does_not_contain_key(rel)



@when(parsers.parse('a client requests the {rel} resource collection'))
def when_a_client_requests_the_rel_resource_collection(api, context, rel):
    context.rel = rel
    url = href_from_resource(context.home, rel)
    response = api.get(url)
    context.resource = response.json

@when(parsers.parse('a client requests a single {rel} resource'))
def when_a_client_requests_a_single_rel_resource(api, context, rel):
    context.rel = rel
    my_id = context.first_person_id if rel == 'people' else context.first_car_id
    response = api.get(f'/{rel}/{my_id}')
    context.resource = response.json

@when('a client requests the cars belonging to one of the people collection')
def when_a_client_requests_the_cars_belonging_to_one_of_the_people_collection(api, context):
    response = api.get(f'/people/{context.first_person_id}/cars')
    context.resource = response.json


@when(parsers.parse('a client adds a single {rel} resource'))
def when_a_client_adds_a_single_rel_resource(api, context, rel):
    person = {
        'name': rel
    }
    response = api.post(f'/{rel}/', data=json.dumps(person), content_type='application/json')
    context.resource = response.json

@when('a client adds to the cars belonging to one of the people collection')
def when_a_client_adds_to_the_cars_belonging_to_one_of_the_people_collection(api, context):
    car = {
        'name': 'a car'
    }
    response = api.post(f'/people/{context.first_person_id}/cars', data=json.dumps(car), content_type='application/json')
    context.resource = response.json



@then('its _links property includes')
def then_its_links_property_includes(context, datatable):
    validate_links(context, context.resource, datatable)

@then('its _embedded property includes')
def then_its_embedded_property_includes(context, datatable):
    embedded = context.resource.get('_embedded', {})
    for row in datatable[1:]:  # peel off header row
        rel, type, count = row
        assert_that(embedded.get(rel, None)).is_type_of(list if type == 'collection' else dict)
        if type == 'collection':
            assert_that(len(embedded.get(rel, []))).is_equal_to(int(count))

@then('the resource has no embedded property')
def then_the_resource_has_no_embedded_property(context):
    assert_that(context.resource.get('_embedded', None)).is_none()


@then(parsers.parse('each _embedded {rel} has a _links property with'))
def then_each_embedded_rel_has_a_links_property_with(context, rel, datatable):
    embedded = context.resource.get('_embedded', {}).get(rel, {})
    if isinstance(embedded, dict):
        validate_links(context, embedded, datatable)
    else:
        for item in embedded:
            validate_links(context, item, datatable)


@then('the following _links do not appear')
def then_the_following_links_do_not_appear(context, datatable):
    validate_no_unacceptable_links(context.resource, datatable)


@then(parsers.parse('each _embedded {rel} _links property does not include'))
def then_each_embedded_rel_links_property_does_not_include(context, datatable, rel):
    embedded = context.resource.get('_embedded', {}).get(rel, {})
    if isinstance(embedded, dict):
        validate_no_unacceptable_links(embedded, datatable)
    else:
        for item in embedded:
            validate_no_unacceptable_links(item, datatable)
