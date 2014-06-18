from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy
from mptt.models import MPTTModel, TreeForeignKey


def get_app_choices():
    from routes.apphook_pool import apphook_pool
    return apphook_pool.app_choices


class Route(MPTTModel):
    APP_CHOICES = ()

    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('Slug'), max_length=128, blank=True, null=True)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children',
        verbose_name=_('Parent'))

    cached_pattern = models.CharField(max_length=512, editable=False,
                                      blank=True, null=True)
    app = models.CharField(_('App'), max_length=256, choices=APP_CHOICES,
                           blank=True, null=True)

    order = models.PositiveIntegerField()

    def get_relative_url(self):
        url = "{}".format(self.slug)
        item = self
        while item.parent:
            url = "{}/{}".format(item.parent.slug, url)
            item = item.parent

        return url

    def clean_slug(self):
        if self.slug and self.slug[-1] == '/':
            self.slug = self.slug[0:-1]

    # Overrides
    def __unicode__(self):
        return u'{}'.format(self.name)

    def __init__(self, *args, **kwargs):
        super(Route, self).__init__(*args, **kwargs)
        # TODO UGLY
        self._meta.get_field_by_name('app')[0]._choices = lazy(
            get_app_choices, list)()

    def save(self, *args, **kwargs):
        self.clean_slug()
        self.cached_pattern = self.get_relative_url()
        super(Route, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('parent', 'slug'), )

    class MPTTMeta:
        order_insertion_by = ['order']
