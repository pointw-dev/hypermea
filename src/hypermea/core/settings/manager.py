import logging
import os
from typing import Optional, Callable
from hypermea.core.utils import Singleton

LOG = logging.getLogger('settings.manager')


@Singleton
class SettingsManager:
    """
    A collection of grouped name/value pairs that act as setting/configuration items.
    Groups are identified by a prefix.

    This class is a singleton and can only be used via its instance() method.

    These name/value pairs must first be created.  They can be set in three ways:
    - through this class's methods
    - overridden by environment variables
    - overridden by the contents of an optional file named `_env.conf`
        Each line in the _env.conf is in the format "name=value".
        Blank/whitespace lines and lines staring with # are ignored.

    Methods:
      create                  Adds a group and a name to the collection, with an
                              optional default_value.  Set `is_optional` to True
                              and this setting will not be visible when its value
                              is None

      set_prefix_description  Provide a textual description for a prefix which will
                              be displayed when dumping

      get                     Used to look up the value of a setting.  If the setting name
                              you want to look up has the prefix in it, leave `prefix` None
                              and the method will parse
                              e.g.
                                  prefix == None, setting_name == HY_INSTANCE_NAME
                                     becomes
                                  prefix == HY, setting_name == INSTANCE_NAME

      has_enabled             A value is considered "enabled" if it begins with Y, T, or E
                              i.e. the following means a setting (if it exists) is enabled:
                              - 'Yes' or 'yes' or 'Y' or 'y'
                              - 'True' or 'true' or 'T' or 't'
                              - 'Enabled' or 'enabled' or 'E' or 'e'

      dump                    output all settings by group/prefix.
                              If you do not supply a callback, the method will use print()
                              This gives you the ability to pass callback=LOG.info to
                              redirect the dump output to your logger

      []                      You can use square brackets to access (and change) settings
                              whose name has the begins with the prefix
                              e.g.
                                  port = settings['HY_API_PORT']
                                  settings['HY_LOGGING_LEVEL'] = 'Debug'
    """

    def __init__(self):
        self.settings = {}
        self.optional_settings = {}
        self.prefix_descriptions = {}

    # __OVERLOADS__
    def __getitem__(self, setting_name):
        return self.get(setting_name)

    def __setitem__(self, setting_name, value):
        prefix, setting_name = self._parse_setting_name(setting_name)
        if prefix in self.settings and setting_name in self.settings[prefix]:
            self.settings[prefix][setting_name] = value
        else:
            raise ValueError(f'{prefix}_{setting_name} does not exist - create it first before assigning a value')

    def __contains__(self, setting_name):
        prefix, setting_name = self._parse_setting_name(setting_name)
        return prefix in self.settings and setting_name in self.settings[prefix]

    # PUBLIC METHODS
    def create(self, prefix: str, setting_name: str, default_value: str = None, is_optional: bool = False):
        prefix = prefix.upper()
        if prefix not in self.settings:
            self.settings[prefix] = {}
        if is_optional and prefix not in self.optional_settings:
            self.optional_settings[prefix] = {}

        if type(setting_name) is dict:  # is_optional is ignored
            settings = setting_name
            for setting_name in settings:
                if setting_name.upper() in self.settings[prefix]:
                    raise ValueError(f'settings[{prefix}][{setting_name.upper()}] already exists')
                self.settings[prefix][setting_name.upper()] = settings[setting_name]
        else:
            setting_name = setting_name.upper()
            if setting_name in self.settings[prefix]:
                raise ValueError(f'settings[{prefix}][{setting_name}] already exists')
            if is_optional:
                self.optional_settings[prefix][setting_name] = default_value
            else:
                self.settings[prefix][setting_name] = default_value

    def set_prefix_description(self, prefix: str, description: str):
        prefix = prefix.upper()
        if prefix not in self.settings:
            self.settings[prefix] = {}
        if prefix not in self.prefix_descriptions:
            self.prefix_descriptions[prefix] = ''
        self.prefix_descriptions[prefix] = description

    def get(self, setting_name: str, default_value: str = None):
        self._set_from_environment()
        setting_name = setting_name.upper()
        prefix, setting_name = self._parse_setting_name(setting_name)

        return self.settings.get(prefix, {}).get(setting_name, default_value)

    def sanitized_settings(self):
        rtn = {}
        for prefix in self.settings:
            rtn[prefix] = {
                'settings': []
            }
            if prefix in self.prefix_descriptions:
                rtn[prefix]['description'] = self.prefix_descriptions[prefix]
            for setting_name in sorted(self.settings[prefix]):
                value = self.settings[prefix][setting_name]
                if ('PASSWORD' in setting_name) or ('SECRET' in setting_name) or ('PRIVATE' in setting_name):
                    value = '***'
                rtn[prefix][setting_name] = value
        return rtn

    def dump(self, prefix=None, callback: Optional[Callable[[str], None]] = None):
        self._set_from_environment()
        if not callback:
            callback = print

        settings = self.sanitized_settings()
        for prefix in settings:
            if 'description' in settings[prefix]:
                callback(f"== {prefix}: {settings[prefix]['description']}")
            for setting_name in [setting for setting in sorted(settings[prefix]) if setting not in ['description', 'settings']]:
                value = settings[prefix][setting_name]
                callback(f'{prefix}_{setting_name}: {value}')

        if self.settings.get('HY_BASE_URL') and self.settings.get('HY_BASE_PATH'):
            LOG.warning('HY_BASE_URL and HY_BASE_PATH cannot both be set.  Ignoring HY_BASE_PATH.')

    def has_enabled(self, setting_name: str) -> bool:
        value = self.get(setting_name)
        if not value:
            return False
        return value[0].upper() in 'YTE' if value else False
        # i.e. the following means a setting (if it exists) is enabled:
        # - 'Yes' or 'yes' or 'Y' or 'y'
        # - 'True' or 'true' or 'T' or 't'
        # - 'Enabled' or 'enabled' or 'E' or 'e'

    # _PRIVATE METHODS
    def _set_from_environment(self):
        if os.path.exists('_env.conf'):
            with open('_env.conf') as setting:
                for line in setting:
                    if not line.startswith('#'):
                        line = line.rstrip()
                        nvp = line.split('=')
                        if len(nvp) == 2:
                            os.environ[nvp[0].strip()] = nvp[1].strip()

        for prefix in self.settings:
            for setting_name in self.settings[prefix]:
                old_value = self.settings[prefix][setting_name]  # TODO: refactor with optional below
                new_value = os.environ.get(f'{prefix}_{setting_name}', self.settings[prefix][setting_name])
                if old_value and not isinstance(old_value, str):
                    try:
                        new_value = type(old_value)(new_value)
                    except ValueError:
                        raise TypeError(
                            f'attempt to set {prefix}_{setting_name} to a different type than its default value (should be {type(old_value)}).')
                self.settings[prefix][setting_name] = new_value

        for prefix in self.optional_settings:
            for setting_name in self.optional_settings[prefix]:
                old_value = self.optional_settings[prefix][setting_name]  # TODO: refactor with non-optional above
                new_value = os.environ.get(f'{prefix}_{setting_name}')
                if new_value:
                    if not isinstance(old_value, str) and not isinstance(old_value, type(None)):
                        try:
                            new_value = type(old_value)(new_value)
                        except ValueError:
                            raise TypeError(
                                f'attempt to set {prefix}_{setting_name} to a different type than its default value (should be {type(old_value)}).')

                    if new_value:
                        self.settings[prefix][setting_name] = new_value

    @staticmethod
    def _parse_setting_name(setting_name):
        first_underscore = setting_name.index('_')
        prefix = setting_name[:first_underscore]
        setting_name = setting_name[first_underscore + 1:]
        return prefix, setting_name


# TODO: handle cancellable values
