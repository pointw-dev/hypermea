from typing import Any, Optional
from pydantic import Field


# noinspection PyPep8Naming
def SecretField(*, default: Any = ..., description: str = "", alias: Optional[str] = None):
    return Field(
        default=default,
        alias=alias,
        description=description,
        json_schema_extra={"sensitive": True}
    )
