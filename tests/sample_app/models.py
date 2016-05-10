# -*- coding: utf-8 -*-
from django.db import models

from meta_tagger.models import MetaTagMixin


class NewsArticle(MetaTagMixin):
    title = models.CharField(max_length=255, verbose_name='Title')
