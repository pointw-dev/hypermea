from typing import Optional
from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.helpers import SecretField


class RedisSettings(BaseSettings):
    """
    Connection settings to the Redis server.
    """
    model_config = SettingsConfigDict(env_prefix='REDIS_')

    host: str = Field(
        default='localhost',
        description='Redis host.'
    )
    port: int = Field(
        default=6379,
        description='Redis port.'
    )
    db: int = Field(
        default=0,
        description="The database number this service will use."
    )

    # credentials
    username: Optional[str] = SecretField(
        default=None,
        description='Redis username.'
    )
    password: Optional[SecretStr] = SecretField(
        default=None,
        description='Redis password.'
    )


    @model_validator(mode='after')
    def ensure_credentials_pair(self) -> 'MongoSettings':
        user_set = self.username is not None
        pass_set = self.password is not None

        if user_set != pass_set:
            raise ValueError('Mongo username and password must both be set or both be omitted.')
        return self
