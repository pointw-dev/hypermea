from hypermea.core.settings import SettingsManager
SETTINGS = SettingsManager.instance()


SETTINGS.set_prefix_description('{$prefix}', 'Auth0 configuration')
SETTINGS.create('{$prefix}', {
    'API_AUDIENCE': 'https://{$project_name}.us.auth0.com/api/v2/',
    'API_BASE_URL': 'https://{$project_name}.us.auth0.com/api/v2',
    'CLAIMS_NAMESPACE': 'https://pointw.com/{$project_name}',
    'TOKEN_ENDPOINT': 'https://{$project_name}.us.auth0.com/oauth/token',
    'CLIENT_ID': '--your-client-id--',
    'CLIENT_SECRET': '--your-client-secret--'
})

