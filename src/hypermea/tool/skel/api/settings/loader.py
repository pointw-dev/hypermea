from pathlib import Path
from typing import Type
from dotenv import dotenv_values, load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings


def get_env_var_name(model: Type[BaseSettings], field_name: str) -> str:
    prefix = model.model_config.get("env_prefix", "")
    return f"{prefix}{field_name}".upper()


def is_field_sensitive(field) -> bool:
    """Determine if a field is sensitive based on its annotation or extra metadata."""
    return (
        field.annotation is SecretStr
        or (field.json_schema_extra or {}).get("sensitive", False)
    )


def check_file_for_secrets(model: Type[BaseSettings], file_path: Path):
    """Ensure sensitive keys do not appear in non-secret files."""
    if "secret" in file_path.name.lower():
        return  # Allowed

    env_vars = dotenv_values(file_path)

    sensitive_keys = {
        get_env_var_name(model, field_name)
        for field_name, field in model.model_fields.items()
        if is_field_sensitive(field)
    }

    for key in env_vars:
        if key.upper() in sensitive_keys:
            raise RuntimeError(
                f"❌ Secret key '{key}' found in non-secret file '{file_path.name}'. "
                f"Move it to a file with 'secret' in the name."
            )


def load_ordered_env_files(models: list[Type[BaseSettings]]):
    for path in sorted(Path(".").glob(".[0-9][0-9]*.env")):
        for model in models:
            check_file_for_secrets(model, path)
        print(f"💡 Loading {path.name}")
        load_dotenv(path, override=True)
