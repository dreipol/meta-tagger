# -*- coding: utf-8 -*-
from cms.extensions import PageExtension, extension_pool
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField


class MetaTagBaseMixin(models.Model):
    class Meta:
        abstract = True

    def get_meta_title(self):
        return getattr(self, 'meta_title', False)

    def get_meta_description(self):
        return getattr(self, 'meta_description', False)

    def get_robots_indexing(self):
        return getattr(self, 'robots_indexing', False)

    def get_robots_following(self):
        return getattr(self, 'robots_following', False)

    def get_og_image(self):
        return getattr(self, 'og_image', None)

    def get_og_image_width(self):
        return getattr(self, 'og_image_width', None)

    def get_og_image_height(self):
        return getattr(self, 'og_image_height', None)


class MetaTagTitleDescriptionMixin(MetaTagBaseMixin):
    meta_title = models.CharField(max_length=255, blank=True, verbose_name=_('Meta title'))
    meta_description = models.CharField(max_length=255, blank=True, verbose_name=_('Meta description'))

    class Meta:
        abstract = True


class RobotsMixin(MetaTagBaseMixin):
    robots_indexing = models.BooleanField(default=True, verbose_name=_('Allow Indexing'))
    robots_following = models.BooleanField(default=True, verbose_name=_('Allow Following'))

    class Meta:
        abstract = True


class OpenGraphMixin(MetaTagBaseMixin):
    og_image = FilerImageField(blank=True, null=True, verbose_name=_('Open Graph image'))
    og_image_width = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Open Graph image width'))
    og_image_height = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Open Graph image height'))

    class Meta:
        abstract = True


class MetaTagMixin(MetaTagTitleDescriptionMixin, RobotsMixin, OpenGraphMixin):
    """
    Use this mixin for your models if you want to make them ready for SEO and social sharing. Make sure you don't
    forget to implement your translation settings before you create your project migrations.
    """
    class Meta:
        abstract = True


class MetaTagPageExtension(OpenGraphMixin, RobotsMixin, PageExtension):
    class Meta:
        verbose_name = 'Meta Tag'

extension_pool.register(MetaTagPageExtension)
