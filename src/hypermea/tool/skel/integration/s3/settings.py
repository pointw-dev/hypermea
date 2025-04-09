from hypermea.core.settings import SettingsManager
SETTINGS = SettingsManager.instance()


SETTINGS.set_prefix_description('{$prefix}', 'Connection details to an AWS S3 bucket')
SETTINGS.create('{$prefix}', {
    'AWS_ACCESS_KEY_ID': '{$access_key}',
    'AWS_SECRET_ACCESS_KEY': '{$secret_key}',
    'AWS_REGION': '{$region}',
    'BUCKET_NAME': '{$bucket}'
})

