from hypermea.core.settings_manager import SettingsManager
import configuration.hypermea_settings
import configuration.api_settings
from .logger_config import additional_log_configuration


SETTINGS = SettingsManager.instance()
VERSION = '0.1.0'
