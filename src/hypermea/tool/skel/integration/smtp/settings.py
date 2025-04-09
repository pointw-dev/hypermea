from hypermea.core.settings import SettingsManager
SETTINGS = SettingsManager.instance()


SETTINGS.set_prefix_description('SMTP', 'Connection details for the email server')
SETTINGS.create('SMTP', {
    'HOST': 'not configured',
    'PORT': 25
})

SETTINGS.create('SMTP', 'FROM', is_optional=True)
SETTINGS.create('SMTP', 'USE_TLS', is_optional=True)
SETTINGS.create('SMTP', 'USERNAME', is_optional=True)
SETTINGS.create('SMTP', 'PASSWORD', is_optional=True)

