# -*- coding: utf-8 -*-
from django.conf.urls import url
from tests.sample_app.views import NewsArticleDetailView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', NewsArticleDetailView.as_view(), name='news-article-detail'),
]
