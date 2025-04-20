from zoneinfo import ZoneInfo
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class TimezoneSettings(BaseSettings):
    """
    Timezone and datetime behavior configuration.
    """
    model_config = SettingsConfigDict(env_prefix='HY_')

    require_timezone: Optional[bool] = Field(
        default=None,
        description='If true, all incoming datetime values must include timezone info (not yet implemented).'
    )

    assume_timezone: Optional[str] = Field(
        default=None,
        description='If set, naive datetime inputs will be interpreted as being in this timezone (not yet implemented).'
    )

    output_timezone: Optional[str] = Field(
        default=None,
        description='If set, datetime values will be converted to this timezone on output, otherwise they retain their original timezone (not yet implemented).'
    )


    @model_validator(mode='after')
    def check_exclusivity(self) -> 'TimezoneSettings':
        if self.require_timezone and self.assume_timezone:
            raise ValueError(
                "require_timezone=True and assume_timezone both set — these are mutually exclusive."
            )
        return self

    @model_validator(mode='after')
    def validate_timezones(self) -> 'TimezoneSettings':
        if self.require_timezone and self.assume_timezone:
            raise ValueError("require_timezone=True and assume_timezone are mutually exclusive.")

        for field in ("assume_timezone", "output_timezone"):
            value = getattr(self, field)
            if value:
                try:
                    ZoneInfo(value)
                except Exception:
                    raise ValueError(f"{field}='{value}' is not a valid timezone identifier.")
        return self
