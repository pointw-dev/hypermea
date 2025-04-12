from typing import Optional
from pydantic import SecretStr, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SmtpSettings(BaseSettings):
    """
    Connection details for the email server.
    """
    model_config = SettingsConfigDict(env_prefix='SMTP_')

    host: Optional[str] = Field(
        default=None,
        description='SMTP server hostname or IP address.'
    )
    port: Optional[int] = Field(
        default=25,
        description='SMTP server port number.'
    )
    sender: str = Field(
        default='alerts@example.com',
        description='Who the emails are sent from.'
    )

    use_tls: bool = Field(
        default=False,
        description='Use TLS'
    )
    username: Optional[str] = Field(
        default=None,
        description='SMTP username.'
    )
    password: Optional[SecretStr] = Field(
        default=None,
        description='SMTP password.'
    )


    @model_validator(mode='after')
    def ensure_credentials_pair(self) -> 'SmtpSettings':
        user_set = self.username is not None
        pass_set = self.password is not None

        if user_set != pass_set:
            raise ValueError('SMTP username and password must both be set or both be omitted.')
        return self
