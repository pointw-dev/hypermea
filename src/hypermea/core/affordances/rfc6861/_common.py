def _schema_to_templates(schema, form_type, resource=None):
    templates = {}
    methods = ['POST']
    if form_type == 'edit':
        methods = ['PUT', 'PATCH']

    for method in methods:
        properties = _schema_to_properties(schema, method, resource)
        template_name = 'patch' if method == 'PATCH' else 'default'
        templates[template_name] = {
            'method': method,
            # 'title': 'Soon is coming',
            'contentType': 'application/json',
            'properties': properties,
        }

    return templates


def _schema_to_properties(schema, method, resource):
    properties = []
    for field, field_info in schema.items():
        if field.startswith('_'):
            continue

        field_type = field_info.get('type', 'string')
        hal_field = {
            'name': field,
            'prompt': f'Enter {field}',
            'required': False if method == 'PATCH' else field_info.get('required', False)
        }
        _process_types(field, field_info, field_type, hal_field, method, resource)
        _add_validators(field, field_info, field_type, hal_field, resource)

        properties.append(hal_field)
    return properties


def _process_types(field, field_info, field_type, hal_field, method, resource):
    if field_type == 'dict':
        _process_complex_type('object', field, field_info, hal_field, method, resource)
    elif field_type == 'list':
        _process_complex_type('array', field, field_info, hal_field, method, resource)
    elif field_type == 'integer':
        hal_field['type'] = 'number'
    else:
        if resource and field in resource:
            hal_field['value'] = resource[field]
        hal_field['type'] = field_type


def _process_complex_type(property_type, field, field_info, hal_field, method, resource):
    hal_field['type'] = property_type
    if 'schema' in field_info:
        hal_field['items'] = _schema_to_properties(
            field_info['schema'],
            method,
            resource.get(field) if resource else None
        )


def _add_validators(field, field_info, field_type, hal_field, resource):
    if field_info.get('allow_unknown'):
        hal_field['hyAnyObject'] = True
    else:
        _handle_allowed(field, field_info, hal_field, resource)

        if 'readonly' in field_info:
            hal_field['readonly'] = True if field_info['readonly'] else False

        if 'min' in field_info:
            hal_field['min'] = field_info['min']

        if 'max' in field_info:
            hal_field['max'] = field_info['max']

        if 'maxlength' in field_info:
            hal_field['maxLength'] = field_info['maxlength']

        if 'minlength' in field_info:
            hal_field['minLength'] = field_info['minlength']

        if 'regex' in field_info:
            hal_field['pattern'] = field_info['regex']

        if field_type == 'datetime':
            hal_field['format'] = 'date-time'


def _handle_allowed(field, field_info, hal_field, resource):
    if 'allowed' in field_info:
        hal_field['options'] = {
            'inline': field_info['allowed'],
            'maxItems': 1
        }
        if 'default' in field_info:
            hal_field['options']['selectedValues'] = [field_info['default']]
        if resource and field in resource:
            hal_field['options']['selectedValues'] = [resource[field]]


def generate_hal_form(form_type, schema, self_ref, resource=None):
    if form_type not in ['edit', 'create']:
        raise ValueError(f'unrecognized form type: {form_type}')

    form = {
        '_links': {'self': {'href': self_ref}},
        '_templates': _schema_to_templates(schema, form_type, resource)
    }
    return form


def get_allowed_methods(app, collection_name):
    global_resource_methods = app.config.get('RESOURCE_METHODS', [])
    global_item_methods = app.config.get('ITEM_METHODS', [])

    resource_definition = app.config['DOMAIN'].get(collection_name, {})
    resource_methods = resource_definition.get('resource_methods', global_resource_methods)
    item_methods = resource_definition.get('item_methods', global_item_methods)

    return {
        'resource_methods': resource_methods,
        'item_methods': item_methods
    }
