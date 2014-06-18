from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Route

# django-suit support
try:
    from suit.admin import SortableModelAdmin
except:
    class SortableModelAdmin(object):
        pass


class RouteAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    list_display = ('name', )
    prepopulated_fields = {"slug": ("name",)}
    sortable = 'order'

admin.site.register(Route, RouteAdmin)
