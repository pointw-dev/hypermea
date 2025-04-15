import importlib.util
import inspect
import os
import sys
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import BaseModel
from pydantic.fields import PydanticUndefined
from typing import Dict, Type, Any, get_args, get_origin, Literal, List

from hypermea.tool import get_singular_plural

from .resource_model import ResourceModel
from .relation import Relation
from .resource_ref import ResourceRef, external, local

ALPHA_NUM_REGEX = r'[a-zA-Z0-9]*'
OBJECT_ID_REGEX = r'[a-f0-9]{24}'
TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "float",
    bool: "boolean",
    bytes: "binary",
    list: "list",
    dict: "dict",
    set: "set",
    tuple: "tuple",
    datetime: "datetime",
    date: "date",
    time: "time",
    Decimal: "decimal",
}

def _is_pydantic_model(obj):
    return inspect.isclass(obj) and issubclass(obj, ResourceModel) and obj is not ResourceModel


def _enrich_with_constraints(field_schema: Dict[str, Any], field) -> None:
    for metadata_entry in field.metadata:
        if not isinstance(metadata_entry, dict):
            continue

        if metadata_entry.get("min_length") is not None:
            field_schema["minlength"] = metadata_entry["min_length"]
        if metadata_entry.get("max_length") is not None:
            field_schema["maxlength"] = metadata_entry["max_length"]
        if metadata_entry.get("ge") is not None:
            field_schema["min"] = metadata_entry["ge"]
        if metadata_entry.get("le") is not None:
            field_schema["max"] = metadata_entry["le"]
        if metadata_entry.get("const") is not None:
            field_schema["allowed"] = [metadata_entry["const"]]
        if metadata_entry.get("multiple_of") is not None:
            field_schema["multipleof"] = metadata_entry["multiple_of"]
        if metadata_entry.get("pattern") is not None:
            field_schema["regex"] = metadata_entry["pattern"]
        if metadata_entry.get("enum") is not None:
            field_schema["allowed"] = list(metadata_entry["enum"])


def _pydantic_to_cerberus(model: Type[BaseModel]) -> Dict[str, Any]:
    fields_schema = {}
    for field_name, field in model.model_fields.items():
        field_schema = {}
        python_type = field.annotation
        origin = get_origin(python_type)
        args = get_args(python_type)

        # Determine field type and handle Literal
        if origin is Literal:
            field_schema["type"] = TYPE_MAP.get(type(args[0]), "string")
            field_schema["allowed"] = list(args)
        elif inspect.isclass(python_type) and issubclass(python_type, BaseModel):
            field_schema["type"] = "dict"
            field_schema["schema"] = _pydantic_to_cerberus(python_type)["schema"]
        elif origin in (list, List):
            item_type = args[0]
            field_schema["type"] = "list"
            if inspect.isclass(item_type) and issubclass(item_type, BaseModel):
                field_schema["schema"] = {
                    "type": "dict",
                    "schema": _pydantic_to_cerberus(item_type)["schema"]
                }
            else:
                field_schema["schema"] = {
                    "type": TYPE_MAP.get(item_type, "string")
                }
        else:
            field_schema["type"] = TYPE_MAP.get(python_type, "string")

        # Required/nullable/default logic
        field_schema["required"] = field.is_required()
        if field.default is not PydanticUndefined:
            field_schema["default"] = field.default
        if field.default is None:
            field_schema["nullable"] = True

        _enrich_with_constraints(field_schema, field)

        field_key = field.alias or field_name
        fields_schema[field_key] = field_schema

    return {"schema": fields_schema, "link_relation": model.__name__.lower()}



def _get_domain_path():
    try:
        import domain
        return os.path.dirname(domain.__file__)
    except ModuleNotFoundError:
        return './domain'


def _import_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _discover_resource_models():
    domain_path = _get_domain_path()
    sys.path.insert(0, domain_path)  # to allow import

    discovered = []

    for filename in os.listdir(domain_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            file_path = os.path.join(domain_path, filename)

            module = _import_module_from_path(module_name, file_path)

            for name, obj in inspect.getmembers(module, _is_pydantic_model):
                plural = getattr(getattr(obj, "Config", object), "plural", name.lower())
                discovered.append((plural, obj))

    return discovered


def load_domain() -> Dict[str, Dict[str, Any]]:
    domain_path = _get_domain_path()
    relations_file = os.path.join(domain_path, '_relations.py')
    relations_module = _import_module_from_path('domain', relations_file)
    relation_registry = getattr(relations_module, 'RELATION_REGISTRY', [])

    models = _discover_resource_models()

    domain = {
        name: _pydantic_to_cerberus(obj)
        for name, obj in models
    }

    for rel in relation_registry:
        if rel.child.external:
            continue # no changes to the DOMAIN are required - links added by hooks
        _add_sub_resource_to_domain(domain, models, rel)

    return domain


def _add_sub_resource_to_domain(domain, models, rel):
    child_class = get_resource_model_by_rel(rel.child, models=models)
    child, children = child_class.singplu()
    if rel.parent.external:
        parent, parents = get_singular_plural(str(rel.parent))
        ref_field = f'_{parent}_ref'
        url = f'{children}/{parent}/<regex("{OBJECT_ID_REGEX}"):{ref_field}>'
    else:
        parent_class = get_resource_model_by_rel(rel.parent, models=models)
        parent, parents = parent_class.singplu()
        ref_field = f'_{parent}_ref'
        url = f'{parents}/<regex("{OBJECT_ID_REGEX}"):{ref_field}>/{children}'
    sub_resource = f'{parents}_{children}'
    schema = domain[children]['schema']
    schema[ref_field] = {
        'type': 'objectid',
        'external_relation': {
            'rel': parent,
            'embeddable': True
        }
    } if rel.parent.external else {
        'type': 'objectid',
        'data_relation': {
            'field': '_id',  # TODO: get_id_field?
            'resource': parents,
            'embeddable': True,
        }
    }
    resource_title = f'{children}'
    domain[sub_resource] = {
        'schema': schema,
        'url': url,
        'resource_title': resource_title,
        'datasource': {
            'source': children
        }
    }


def list_domain_resources() -> list[str]:
    return [obj.__name__.lower() for _, obj in _discover_resource_models()]


def get_resource_model_by_rel(rel: str, *, models=None, retry=False):
    model = None
    if models is None:
        models = _discover_resource_models()
    for _, obj in models:
        if obj.__name__.lower().startswith(str(rel).lower()):
            model = obj

    if model is None and not retry:
        # rel s/b singular, but retry as singular for max flexibility and reducing mistakes...
        singular, _ = get_singular_plural(str(rel).lower())
        model = get_resource_model_by_rel(singular, models=models, retry=True)

    return model


__all__ = [
    ResourceModel, Relation, external, local,
    ALPHA_NUM_REGEX, OBJECT_ID_REGEX,
    load_domain, list_domain_resources, get_resource_model_by_rel
]
