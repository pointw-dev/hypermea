from typing import Any
from pydantic import Field


# noinspection PyPep8Naming
def SecretField(*, default: Any = ..., description: str = "", alias: str | None = None):
    return Field(
        default=default,
        alias=alias,
        description=description,
        json_schema_extra={"sensitive": True}
    )

