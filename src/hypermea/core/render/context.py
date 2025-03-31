from flask import request, current_app
from hypermea.core.utils import get_my_base_url, get_id_field, get_resource_rel


class ResourceContext:
    def __init__(self, resource_name, resource_scope, base_url, query_args, domain, schema, id_field, parent, child, resource_rel):
        self.name = resource_name
        self.scope = resource_scope
        self.base_url = base_url
        self.query_args = query_args
        self.domain = domain
        self.schema = schema
        self.id_field = id_field
        self.parent = parent
        self.child = child
        self.rel = resource_rel


    @classmethod
    def from_request(cls, data):
        query_args = request.args
        resource_name, scope = cls._parse_url_rule()
        if request.method  == 'POST':
            scope = 'collection' if (isinstance(data, list) or '_items' in data) else 'item'

        base_url = get_my_base_url()
        domain = current_app.config['DOMAIN']
        schema = domain.get(resource_name, {}).get('schema')
        parent = None
        child = None

        if '_' in resource_name:
            parent, child = resource_name.split('_', 1)
            resource_name = child

        id_field = get_id_field(resource_name) if scope != 'root' else None
        resource_rel = get_resource_rel(resource_name)

        return cls(resource_name, scope, base_url, query_args, domain, schema, id_field, parent, child, resource_rel)

    @staticmethod
    def _parse_url_rule():
        rule_endpoint = request.url_rule.endpoint
        if '|' in rule_endpoint:
            resource_name, scope = rule_endpoint.split('|')
            scope = {
                'resource': 'collection',
                'item_lookup': 'item'
            }.get(scope, scope)
        else:
            resource_name = rule_endpoint
            scope = 'root'
        return resource_name, scope
