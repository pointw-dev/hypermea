from hypermea.core.settings import SettingsManager
SETTINGS = SettingsManager.instance()

SETTINGS.set_prefix_description('{$prefix}', 'Access metadata of media files')
SETTINGS.create('{$prefix}', {
    'FALLBACK_MEDIA_TYPE': ''application/octet-stream''
})
