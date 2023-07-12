def generate_hal_forms_template(method, schema, self_ref='unspecified'):
    template = {'_links': {'self': {'href': self_ref}}}
    properties = {}

    for field, field_info in schema.items():
        if field.startswith('_'):
            continue

        field_type = field_info.get('type')
        hal_field = {
            'name': field,
            'type': field_type,
            'required': field_info.get('required', False),
            'value': '',
        }

        if 'allowed' in field_info:
            hal_field['enum'] = field_info['allowed']

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

        properties[field] = hal_field

    template['_templates'] = {
        'default': {
            'method': method,
            'contentType': 'application/json',
            'properties': properties,
        }
    }

    return template
