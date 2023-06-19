"""
Fields to be added to all resources, other commonly used constants
"""
ALPHA_NUM_REGEX = '[a-zA-Z0-9]*'
OBJECT_ID_REGEX = '[a-f0-9]{24}'

COMMON_FIELDS = {
    '_tenant': {'type': 'string'},
    '_tags': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    '_x': {
        'allow_unknown': True
    }
}
