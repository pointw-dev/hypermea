def generate_hal_forms_template(method, schema, self_ref, resource=None):
    template = {'_links': {'self': {'href': self_ref}}}
    properties = []

    for field, field_info in schema.items():
        if field.startswith('_'):
            continue

        field_type = field_info.get('type', 'string')
        hal_field = {
            'name': field,
            'prompt': f'Enter {field}',
            'type': field_type,
            'required': field_info.get('required', False),
            'value': resource[field] if resource else '',
        }

        if field_info.get('allow_unknown'):
            hal_field['hyAnyObject'] = True
        else:
            if 'allowed' in field_info:
                hal_field['options'] = {
                    'inline': field_info['allowed'],
                    'maxItems': 1
                }
                if 'default' in field_info:
                    hal_field['options']['selectedValues'] = [field_info['default']]
                if field in resource:
                    hal_field['options']['selectedValues'] = [resource[field]]

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

        properties.append(hal_field)

    template['_templates'] = {
        'default': {
            'method': method,
            # 'title': 'Soon is coming',
            'contentType': 'application/json',
            'properties': properties,
        }
    }

    return template
