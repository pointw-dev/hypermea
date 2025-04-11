from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class LoggingSettings(BaseSettings):
    """
    Settings to control how and where log entries are handled.
    """
    model_config = SettingsConfigDict(env_prefix='HY_')

    trace_logging: bool = Field(
        default=True,
        description='Enable/disable trace logging.'
    )
    max_body_size: int = Field(
        default=1024,
        description='The number of characters after which a response or request payload is truncated in the logs.'
    )

    # direct log entries to folder/files
    log_to_folder: bool = Field(
        default=False,
        description='Enable/disable logging to a folder.'
    )
    folder_to_log_to: Optional[str] = Field(
        default=None,
        description='The folder log files will be written to.'
    )

    # direct log entries to emails
    log_to_email: bool = Field(
        default=False,
        description='Enable/disable logging to a email.'
    )
    email_verbosity: str = Field(
        default='ERROR',
        description='The minimum verbosity level a log entry must be before it will be emailed.'
    )
    # log_email_pattern: Optional[str] = Field(
    #     default=None,
    #     description='The regex pattern used against the log entry message, to determine whether a log entry is emailed.'
    # )
    email_recipients: Optional[str] = Field(
        default=None,
        description='A comma separated list of email addresses that will received email logs.'
    )
    email_from: Optional[str] = Field(
        default=None,
        description='The sender email address of log entries.'
    )
