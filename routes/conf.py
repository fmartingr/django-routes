from django.conf import settings

# Routes app module name
APP_MODULE_NAME = getattr(settings, 'ROUTES_APP_MODULE_NAME', 'routes_app')
