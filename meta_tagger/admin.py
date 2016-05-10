# -*- coding: utf-8 -*-
from cms.extensions import PageExtensionAdmin
from django.contrib import admin

from .models import MetaTagPageExtension


admin.site.register(MetaTagPageExtension, PageExtensionAdmin)
