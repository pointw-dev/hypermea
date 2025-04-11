from typing import Union
from pydantic import BaseModel
from settings.hypermea import HypermeaSettings
from settings.logging import LoggingSettings
from settings.rate_limit import RateLimitSettings
from integration.mongo.settings import MongoSettings
from integration.smtp.settings import SmtpSettings


class AllSettings(BaseModel):
    hypermea: HypermeaSettings
    logging: LoggingSettings
    rate_limit: RateLimitSettings
    mongo: MongoSettings
    smtp: SmtpSettings


def get_settings() -> AllSettings:
    from settings import get_hypermea, get_logging, get_rate_limit, get_mongo, get_smtp
    return AllSettings(
        hypermea=get_hypermea(),
        logging=get_logging(),
        rate_limit=get_rate_limit(),
        mongo=get_mongo(),
        smtp=get_smtp(),
    )


def build_settings(
    hypermea: HypermeaSettings = None,
    logging: LoggingSettings = None,
    rate_limit: RateLimitSettings = None,
    mongo: MongoSettings = None,
    smtp: SmtpSettings = None,
) -> AllSettings:
    defaults = get_settings()
    return AllSettings(
        hypermea=hypermea or defaults.hypermea,
        logging=logging or defaults.logging,
        rate_limit=rate_limit or defaults.rate_limit,
        mongo=mongo or defaults.mongo,
        smtp=smtp or defaults.smtp,
    )


def inject_settings(overrides: AllSettings):
    from settings import _registry
    current = get_settings()

    for key, override in overrides.model_dump(exclude_none=True).items():
        base = getattr(current, key)
        merged = {**base.model_dump(), **override}
        _registry[key] = base.__class__(**merged)


def reset_settings():
    from settings import _registry
    all_settings = get_settings()
    for key in _registry:
        _registry[key] = getattr(all_settings, key)


def settings_dump(pretty: bool = False) -> str | dict:
    settings_dict = get_settings().model_dump()
    if pretty:
        import json
        return json.dumps(settings_dict, indent=2)
    return settings_dict
