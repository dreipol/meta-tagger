# -*- coding: utf-8 -*-
from cms.extensions import PageExtension, extension_pool
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField


class OpenGraphMixin(models.Model):
    og_image = FilerImageField(blank=True, null=True, verbose_name=_('Open Graph image'))

    class Meta:
        abstract = True


class RobotsMixin(models.Model):
    robots_indexing = models.BooleanField(default=True, verbose_name=_('Allow Indexing'))
    robots_following = models.BooleanField(default=True, verbose_name=_('Allow Following'))

    class Meta:
        abstract = True


class MetaTagMixin(OpenGraphMixin, RobotsMixin):
    """
    Use this mixin for your models if you want to make them ready for SEO and social sharing. Make sure you don't
    forget to implement your translation settings before you create your project migrations.
    """
    meta_title = models.CharField(max_length=255, blank=True, verbose_name=_('Meta title'))
    meta_description = models.CharField(max_length=255, blank=True, verbose_name=_('Meta description'))

    class Meta:
        abstract = True


class MetaTagPageExtension(OpenGraphMixin, RobotsMixin, PageExtension):
    class Meta:
        verbose_name = 'Meta Tag'


extension_pool.register(MetaTagPageExtension)
