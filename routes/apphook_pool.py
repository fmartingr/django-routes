# -*- coding: utf-8 -*-
import warnings

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.conf import settings

from .app_base import App
import conf
import utils
from .exceptions import AppAlreadyRegistered
# from cms.utils.django_load import load, iterload_objects


class ApphookPool(object):
    def __init__(self):
        self.apphooks = []
        self.apps = {}
        self.discovered = False
        self.app_choices = []

    def register(self, app, discovering_apps=False):
        if self.apphooks and not discovering_apps:
            return

        if app.__name__ in self.apps:
            raise AppAlreadyRegistered(
                'An application %r is already registered' % app.__name__)

        if not issubclass(app, App):
            raise ImproperlyConfigured(
                'Application must inherit from routes.app_base.App, '
                'but %r does not' % app.__name__)

        self.apps[app.__name__] = app

    def discover_apps(self):
        for app in settings.INSTALLED_APPS:
            if 'django.' not in app:  # Exclude django apps
                module_path = '{app}.{module_name}'.format(
                    app=app, module_name=conf.APP_MODULE_NAME
                )
                try:
                    # print(module_path)
                    import_module(module_path)
                    # self.apphooks.append(module_path)
                except ImportError:
                    # Module does not exist
                    pass

        # if self.apphooks:
        #     for cls in iterload_objects(self.apphooks):
        #         try:
        #             self.register(cls, discovering_apps=True)
        #         except AppAlreadyRegistered:
        #             pass

        self.discovered = True

    def get_apphooks(self):
        hooks = []

        if not self.discovered:
            self.discover_apps()

        for app_name in self.apps:
            app = self.apps[app_name]
            self.app_choices.append(
                (utils.get_fullname(app), app.name)
            )

            if app.urls:
                hooks.append((app_name, app.name))

        # Unfortunately, we loose the ordering since we now have a list of
        # tuples. Let's reorder by app_name:
        hooks = sorted(hooks, key=lambda hook: hook[1])

        return hooks

    def get_apphook(self, app_name):
        if not self.discovered:
            self.discover_apps()

        try:
            return self.apps[app_name]
        except KeyError:
            # deprecated: return apphooks registered in db with urlconf name
            # instead of apphook class name
            for app in self.apps.values():
                if app_name in app.urls:
                    return app

        raise ImproperlyConfigured('No registered apphook %r found' % app_name)

    def get_app_urlpatterns(self):
        return []

apphook_pool = ApphookPool()
