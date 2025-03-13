import json
from assertpy import assert_that
from pytest_bdd import scenario, given, when, then


FEATURE_PATH = 'hypermea/sorting.feature'

@given("a resource collection exists")
def step_impl(eve_settings):
    eve_settings['DOMAIN'] = {'people': {'schema': {'name': {'type': 'string'}}}}


@given("a resource has multiple items in its collection")
def step_impl(api):
    people = []
    for name in ['Robert', 'James', 'Cheryl', 'Jessica', 'Cory', 'Michael', 'Catherine', 'Mark', 'Jacqueline', 'Marissa']:
        people.append({'name': name})
    response = api.post(
        '/people',
        data=json.dumps(people),
        headers={'content-type': 'application/json'}
    )
    assert_that(response.status_code).is_equal_to(201)


@then("the collection in the response is sorted accordingly")
def step_impl(context):
    names = [i['name'] for i in context['people']]
    is_sorted = all([True if index == 0 else item >= names[index-1] for index, item in enumerate(names)])
    assert_that(is_sorted).is_equal_to(True)
