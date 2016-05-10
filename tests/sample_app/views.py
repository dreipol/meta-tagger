# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from tests.sample_app.models import NewsArticle


class NewsArticleDetailView(DetailView):
    model = NewsArticle
    template_name = 'meta_tagger/index.html'
