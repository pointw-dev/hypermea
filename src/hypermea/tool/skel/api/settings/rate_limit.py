from typing import Optional, Tuple, Annotated
from pydantic import Field, BaseModel, field_validator, PlainSerializer, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseRateLimit(BaseModel):
    requests: int = Field(
        ...,
        description="The number of requests allowed per time window."
    )
    window: int = Field(
        ...,
        description="The duration of the rate limit window, in seconds."
    )

    @field_validator('requests', 'window')
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Rate limit values must be positive integers")
        return v

    def as_tuple(self) -> Tuple[int, int]:
        return self.requests, self.window

    def __str__(self):
        return f"{self.requests} requests per {self.window}s"


# Helper parser function
def parse_rate_limit(value):
    if isinstance(value, str):
        try:
            if value[0] == '(' and value[-1] == ')':
                value = value[1:-1]
            parts = [int(part.strip()) for part in value.split(",")]
            if len(parts) != 2:
                raise ValueError
            return RateLimit(requests=parts[0], window=parts[1])
        except Exception:
            raise ValueError("Rate limit must be a string in the form '300,900'")
    return value


# Define the wrapped type for use in your settings
RateLimit = Annotated[
    BaseRateLimit,
    BeforeValidator(parse_rate_limit),
    PlainSerializer(lambda v: f"{v.requests},{v.window}", return_type=str)
]


class RateLimitSettings(BaseSettings):
    """
    Settings to limit the allowed rate of requests.
    """
    model_config = SettingsConfigDict(env_prefix='HY_')

    rate_limit_global: Optional[RateLimit] = Field(
        default=None,
        description='Global rate limit applied to all request methods.'
    )
    rate_limit_get: Optional[RateLimit] = Field(
        default=None,
        description='Rate limit applied to GET requests (overrides global if both are set).'
    )
    rate_limit_post: Optional[RateLimit] = Field(
        default=None,
        description='Rate limit applied to POST requests (overrides global if both are set).'
    )
    rate_limit_patch: Optional[RateLimit] = Field(
        default=None,
        description='Rate limit applied to PATCH requests (overrides global if both are set).'
    )
    rate_limit_delete: Optional[RateLimit] = Field(
        default=None,
        description='TRate limit applied to DELETE requests (overrides global if both are set).'
    )
