import ast

class SettingPromoter:
    """
    Promotes Eve settings from dev-time settings into the deploy-time.

    This allows settings that are normally static (defined in `settings.py`) to be overridden at
    deploy time via environment-specific settings, enabling a more flexible deployment model.
    """

    def __init__(self, globals):
        self.globals = globals

    def to_deploy_time(self, eve_setting: str) -> None:
        import settings

        setting = settings.get_hypermea()
        value = getattr(setting, eve_setting.lower(), None)
        if eve_setting.startswith('MONGO'):
            setting = settings.get_mongo()
            value = getattr(setting, eve_setting[6:].lower(), None)

        if eve_setting.startswith('RATE_LIMIT_'):
            setting = settings.get_rate_limit()
            value = getattr(setting, eve_setting[11:].lower(), setting.all_methods)
            if value:
                value = value.as_tuple()

        if value:
            self.globals[eve_setting] = value

    def all_to_deploy_time(self, eve_settings: list[str]) -> None:
        for eve_setting in eve_settings:
            self.to_deploy_time(eve_setting)
