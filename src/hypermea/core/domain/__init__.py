import importlib.util
import inspect
import os
import sys
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import BaseModel
from pydantic.fields import PydanticUndefined
from typing import Dict, Type, Any, get_args, get_origin, Literal, List

from .resource_model import ResourceModel
from .relation import Relation, external, local

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

def is_pydantic_model(obj):
    return inspect.isclass(obj) and issubclass(obj, ResourceModel) and obj is not ResourceModel


def enrich_with_constraints(field_schema: Dict[str, Any], field) -> None:
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


def pydantic_to_cerberus(model: Type[BaseModel]) -> Dict[str, Any]:
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
            field_schema["schema"] = pydantic_to_cerberus(python_type)["schema"]
        elif origin in (list, List):
            item_type = args[0]
            field_schema["type"] = "list"
            if inspect.isclass(item_type) and issubclass(item_type, BaseModel):
                field_schema["schema"] = {
                    "type": "dict",
                    "schema": pydantic_to_cerberus(item_type)["schema"]
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

        enrich_with_constraints(field_schema, field)

        field_key = field.alias or field_name
        fields_schema[field_key] = field_schema

    return {"schema": fields_schema, "link_relation": model.__name__.lower()}


def _discover_resource_models():
    # TODO: this is hacky - find a better way to ensure when called from commands._resource.get_resource_list
    try:
        import domain
        domain_path = os.path.dirname(domain.__file__)
    except ModuleNotFoundError:
        domain_path = './domain'

    sys.path.insert(0, domain_path)  # to allow import

    discovered = []

    for filename in os.listdir(domain_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            file_path = os.path.join(domain_path, filename)

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


            for name, obj in inspect.getmembers(module, is_pydantic_model):
                plural = getattr(getattr(obj, "Config", object), "plural", name.lower())
                discovered.append((plural, obj))

    return discovered


def load_domain() -> Dict[str, Dict[str, Any]]:
    return {name: pydantic_to_cerberus(obj) for name, obj in _discover_resource_models()}


def list_domain_resources() -> list[str]:
    return [obj.__name__.lower() for _, obj in _discover_resource_models()]
