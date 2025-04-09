from hypermea.core.settings import SettingsManager
SETTINGS = SettingsManager.instance()


SETTINGS.set_prefix_description('{$prefix}', '--description--')
SETTINGS.create('{$prefix}', {
    'setting1': 'default_value',
    'setting2': 8080
})
