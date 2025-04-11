import socket
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class HypermeaSettings(BaseSettings):
    """
    Settings for the base operation of a hypermea service.
    """
    model_config = SettingsConfigDict(env_prefix='HY_')

    # service settings
    api_name: Optional[str] = Field(
        default='{$project_name}',
        description='The name of this service, used in reports, logs, and in the home resource.'
    )
    api_port: int = Field(
        default=2112,
        description='The port this service is listening on.'
    )
    instance_name: str = Field(
        default_factory=socket.gethostname,
        description='The name of this instance of the service, e.g. "Staging instance on host1".'
    )
    use_absolute_urls: Optional[bool] = Field(
        default=None,
        description='When enabled all link hrefs are fully qualified.'
    )
    base_url: Optional[str] = Field(
        default=None,
        description='The base URL for creating fully qualified hrefs.'
    )
    # TODO: resolve this apparent redundancy
    url_prefix: Optional[str] = Field(
        default=None,
        description='An additional path segment added to the beginning of the URL path of all endpoints.'
    )
    base_path: Optional[str] = Field(
        default=None,
        description='An additional path segment added to the beginning of the URL path of all endpoints.'
    )

    # pagination
    pagination_limit: int = Field(
        default=3000,
        description='The maximum number of items per page returned from a resource collection.  Max page query string requests higher than this value will be treated as this value.'
    )
    pagination_default: int = Field(
        default=1000,
        description='The default number of items per page returned from a resource collection.'
    )

    # caching
    cache_control: Optional[str] = Field(
        default=None,
        description='Cache control for this service.'
    )
    cache_expires: int = Field(
        default=0,
        description='Cache expiration time in seconds.'
    )

    # RFC 6861 affordances
    disable_rfc6861: Optional[bool] = Field(
        default=None,
        description='Turns off _links for create-form, edit-form.'
    )

    # gateway
    gateway_url: Optional[str] = Field(
        default=None,
        description='The URL for the hypermea-gateway this service will register with.'
    )
    name_on_gateway: Optional[str] = Field(
        default=None,
        description="The gateway will use this name for this service's curies."
    )

    # media content
    media_base_url: Optional[str] = Field(
        default=None,
        description='The base URL to be used to generate hrefs to media/content provided by the service.'
    )

    add_echo: bool = Field(
        default=False,
        description='When enabled, the "/_echo" endpoint becomes available to send echo messages to.'
    )
