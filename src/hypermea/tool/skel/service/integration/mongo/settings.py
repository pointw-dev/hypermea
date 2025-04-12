from typing import Optional
from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.helpers import SecretField


class MongoSettings(BaseSettings):
    """
    Connection settings for MongoDB.
    """
    model_config = SettingsConfigDict(env_prefix='MONGO_')

    host: str = Field(
        default='localhost',
        description='MongoDB host.'
    )
    port: int = Field(
        default=27017,
        description='MongoDB port.'
    )
    dbname: str = Field(
        default='{$project_name}',
        description="The name of the database this service's collections will be stored in."
    )
    atlas: Optional[bool] = Field(
        default=False,
        description="Enable if this service will be connecting to a MongoDB Atlas database."
    )

    # credentials
    username: Optional[str] = SecretField(
        default=None,
        description='MongoDB username.'
    )
    password: Optional[SecretStr] = SecretField(
        default=None,
        description='MongoDB password.'
    )

    auth_source: Optional[str] = SecretField(
        default=None,
        description='The database this service uses to store authorized user accounts.'
    )

    @model_validator(mode='after')
    def ensure_credentials_pair(self) -> 'MongoSettings':
        user_set = self.username is not None
        pass_set = self.password is not None

        if user_set != pass_set:
            raise ValueError('Mongo username and password must both be set or both be omitted.')
        return self


"""
from urllib.parse import quote_plus

class MongoSettings(BaseModel):
    mode: Literal['standard', 'atlas'] = Field('standard', alias='MONGO_MODE')

    # Common
    dbname: Optional[str] = Field(default=None, alias='MONGO_DBNAME')

    # Atlas
    uri: Optional[str] = Field(default=None, alias='MONGO_URI')

    # Standard
    host: str = Field('localhost', alias='MONGO_HOST')
    port: int = Field(27017, alias='MONGO_PORT')
    username: Optional[str] = Field(default=None, alias='MONGO_USERNAME')
    password: Optional[str] = Field(default=None, alias='MONGO_PASSWORD')
    auth_source: Optional[str] = Field(default=None, alias='MONGO_AUTH_SOURCE')

    @model_validator(mode='after')
    def validate_by_mode(self) -> 'MongoSettings':
        if self.mode == 'atlas' and not self.uri:
            raise ValueError('MONGO_URI must be set when MONGO_MODE=atlas')
        if self.mode == 'standard' and not self.host:
            raise ValueError('MONGO_HOST must be set when MONGO_MODE=standard')
        return self

    def get_connection_uri(self) -> str:
        if self.mode == 'atlas':
            return self.uri

        creds = ''
        if self.username and self.password:
            creds = f'{quote_plus(self.username)}:{quote_plus(self.password)}@'

        db_part = f'/{self.dbname or ''}'
        auth_part = f'?authSource={self.auth_source}' if self.auth_source else ''

        return f'mongodb://{creds}{self.host}:{self.port}{db_part}{auth_part}'
"""


"""
from hypermea.settings import settings
from pymongo import MongoClient

client = MongoClient(settings.mongo.get_connection_uri())
db = client.get_default_database()  # if dbname provided
"""