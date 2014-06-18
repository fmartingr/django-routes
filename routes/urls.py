from .apphook_pool import apphook_pool
# from django.conf.urls import patterns


urlpatterns = []

if apphook_pool.get_apphooks():
    """
    If there are application urls, add resolver so we have reverse() support.
    TODO
    """
    urlpatterns += apphook_pool.get_app_urlpatterns()
