from hypermea.settings_manager import SettingsManager

PREFIX = 'API'
SETTINGS = SettingsManager.instance()
SETTINGS.set_prefix_description(PREFIX, 'description')
SETTINGS.create(PREFIX, {
    # add settings here
})
