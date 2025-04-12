from typing import Optional
from pydantic import SecretStr, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class {$integration}Settings(BaseSettings):
    """
    Connection details to an AWS S3 bucket.
    """
    model_config = SettingsConfigDict(env_prefix='{$prefix}}')

    setting: str = Field(
        default='value',
        description='Add your settings here.'
    )
