# -*- coding: utf-8 -*-
from cms.extensions import PageExtensionAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import MetaTagPageExtension


@admin.register(MetaTagPageExtension)
class MetaPageExtensionAdmin(PageExtensionAdmin):
    fieldsets = (
        (_('Search Engines'), {
            'fields': ('robots_indexing', 'robots_following', 'robots_disallow')
        }),
        (_('Open Graph'), {
            'fields': ('og_image', ('og_image_width', 'og_image_height'))
        })
    )
