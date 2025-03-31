from flask import request, current_app
from hypermea.core.utils import get_my_base_url, get_id_field, get_resource_rel


class HalResourceContext:
    def __init__(self, resource_name, resource_scope, base_url, domain, schema, id_field, parent, child, resource_rel):
        self.name = resource_name
        self.scope = resource_scope
        self.base_url = base_url
        self.domain = domain
        self.schema = schema
        self.id_field = id_field
        self.parent = parent
        self.child = child
        self.rel = resource_rel


    @classmethod
    def from_request(cls, data):
        resource_name, scope = cls._parse_url_rule()
        if request.method  == 'POST':
            scope = 'collection' if (isinstance(data, list) or '_items' in data) else 'item'

        base_url = get_my_base_url()
        domain = current_app.config['DOMAIN']
        schema = domain.get(resource_name, {}).get('schema')
        resource_rel = get_resource_rel(resource_name)

        if '_' in resource_name:
            parent, child = resource_name.split('_', 1)
            resource_name = child
        self.id_field = get_id_field(self.name) if scope != 'root' else None

        return cls(resource_name, scope, base_url, domain, schema, id_field, parent, child, resource_rel)

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
