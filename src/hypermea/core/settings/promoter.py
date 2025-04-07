import ast

class SettingPromoter:
    """
    Promotes Eve settings from dev-time configuration into the deploy-time.

    This allows settings that are normally static (defined in `settings.py`) to be overridden at
    deploy time via environment-specific configuration, enabling a more flexible deployment model.

    e.g.

        promote = SettingPromoter(globals())
        promote.to_deploy_time("PAGINATION_LIMIT")

    This reads the value of HY_{EVE_SETTING} from the deploy-time `SETTINGS` dict
    and assigns it into the global symbol table as if it were a native dev-time setting.
    """

    def __init__(self, globals):
        self.globals = globals

    def to_deploy_time(self, eve_setting: str) -> None:
        from configuration import SETTINGS

        key = f'HY_{eve_setting}'
        if key in SETTINGS:
            value = SETTINGS[key]
            if eve_setting.startswith('RATE_LIMIT_'):
                value = ast.literal_eval(value)
            self.globals[eve_setting] = value

    def all_to_deploy_time(self, eve_settings: list[str]) -> None:
        for eve_setting in eve_settings:
            self.to_deploy_time(eve_setting)
