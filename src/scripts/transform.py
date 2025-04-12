#!/usr/bin/env python

from hypermea.tool.code_gen.settings_inserter import SettingsInserter



# SettingsInserter('settings', 'ApiSettings').transform('../service/settings/__init__.py')
SettingsInserter('integration', 'S3Settings').transform('../service/settings/__init__.py')
