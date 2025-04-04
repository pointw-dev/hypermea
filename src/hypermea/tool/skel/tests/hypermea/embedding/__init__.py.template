from pytest_bdd import given, when, then, parsers
from tests import *
from tests.hypermea import *

FEATURE = 'hypermea/embedding.feature'

@then('the parent item has no embedded property')
def then_the_parent_item_has_no_embedded_property(context):
    assert_that(context.resource).does_not_contain('_embedded')

@then('the child item has no embedded property')
def then_the_child_item_has_no_embedded_property(context):
    assert_that(context.resource).does_not_contain('_embedded')


@then("the collection is in the response in the embedded property with the appropriate link relation")
def then_the_collection_is_in_the_response_in_the_embedded_property_with_the_appropriate_link_relation(context):
    assert_that(context.collection).contains_key('_embedded')
    assert_that(context.collection['_embedded']).contains_key(context.rel)
    assert_that(context.collection['_embedded'][context.rel]).is_type_of(list)
