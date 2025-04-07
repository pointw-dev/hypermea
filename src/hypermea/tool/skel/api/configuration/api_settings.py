from hypermea.core.settings import SettingsManager

PREFIX = 'API'
SETTINGS = SettingsManager.instance()
SETTINGS.set_prefix_description(PREFIX, 'Settings for {$project_name}')
SETTINGS.create(PREFIX, {
    # add settings here
})
