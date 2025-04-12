from typing import Optional
from pydantic import SecretStr, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseSettings):
    """
    Connection details to an AWS S3 bucket.
    """
    model_config = SettingsConfigDict(env_prefix='S3_')

    region: str = Field(
        default='{$region}',
        description='The AWS region the S3 bucket is in.'
    )

    bucket: str = Field(
        default='{$bucket}',
        description='The name of the S3 bucket.'
    )

    access_key: Optional[str] = SecretField(
        default='{$access_key}',
        description='The access key needed to access the S3 bucket.'
    )
    secret_access_key: Optional[SecretStr] = SecretField(
        default='{$secret_key}',
        description='The secret access key needed to access the S3 bucket.'
    )
