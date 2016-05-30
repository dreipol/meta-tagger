#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase
from django.core.urlresolvers import reverse
from django.test import override_settings
from pyquery import PyQuery
from tests.sample_app.models import NewsArticle

from meta_tagger.models import MetaTagPageExtension


class MetaTaggerViewTestMixin(CMSTestCase):
    def setUp(self):
        self.page_title = 'Test Page Extension'
        self.page_description = 'This is my meta description.'
        self.meta_settings = self._create_settings()
        self.page = self._create_page()

    def _create_settings(self):
        return {
            'META_AUTHOR': 'My meta author',
            'META_PUBLISHER': 'My meta publisher',
            'META_COPYRIGHT': 'My meta copyright',
            'META_COMPANY': 'My meta company',
            'META_SITE_NAME': 'My meta site name',
            'META_TYPE': 'My meta type',
        }

    def _create_page(self):
        return create_page(
            title=self.page_title,
            template='meta_tagger/index.html',
            language='en',
            meta_description=self.page_description,
            published=True
        )

    def _register_apphook(self):
        self.page.application_urls = 'SampleApphook'
        self.page.publish('en')


class GlobalMetaTagTests(MetaTaggerViewTestMixin):
    def test_open_graph_page_url(self):
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[property="og:url"]').attr('content'), 'http://testserver/')

    def test_open_graph_model_url(self):
        self._register_apphook()
        news_article = NewsArticle.objects.create(title='My title', meta_title='My meta title')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(
            content.find('meta[property="og:url"]').attr('content'),
            'http://testserver{}'.format(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        )


class SettingMetaTagTests(MetaTaggerViewTestMixin):
    def test_author(self):
        with self.settings(META_TAGGER_META_TAG_CONF=self.meta_settings):
            response = self.client.get('/')
            content = PyQuery(response.content)
            self.assertEqual(content.find('meta[name="author"]').attr('content'), self.meta_settings['META_AUTHOR'])

    def test_publisher(self):
        with self.settings(META_TAGGER_META_TAG_CONF=self.meta_settings):
            response = self.client.get('/')
            content = PyQuery(response.content)
            self.assertEqual(
                content.find('meta[name="publisher"]').attr('content'),
                self.meta_settings['META_PUBLISHER']
            )

    def test_copyright(self):
        with self.settings(META_TAGGER_META_TAG_CONF=self.meta_settings):
            response = self.client.get('/')
            content = PyQuery(response.content)
            self.assertEqual(
                content.find('meta[name="copyright"]').attr('content'),
                self.meta_settings['META_COPYRIGHT']
            )

    def test_company(self):
        with self.settings(META_TAGGER_META_TAG_CONF=self.meta_settings):
            response = self.client.get('/')
            content = PyQuery(response.content)
            self.assertEqual(content.find('meta[name="company"]').attr('content'), self.meta_settings['META_COMPANY'])

    def test_open_graph_site_name(self):
        with self.settings(META_TAGGER_META_TAG_CONF=self.meta_settings):
            response = self.client.get('/')
            content = PyQuery(response.content)
            self.assertEqual(
                content.find('meta[property="og:site_name"]').attr('content'),
                self.meta_settings['META_SITE_NAME']
            )

    def test_open_graph_type(self):
        with self.settings(META_TAGGER_META_TAG_CONF=self.meta_settings):
            response = self.client.get('/')
            content = PyQuery(response.content)
            self.assertEqual(content.find('meta[property="og:type"]').attr('content'), self.meta_settings['META_TYPE'])


class PageMetaTagTests(MetaTaggerViewTestMixin):
    def test_title(self):
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('title')[0].text, self.page_title)

    def test_description(self):
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="description"]').attr('content'), self.page_description)

    def test_robots_are_inactive_without_whitelist(self):
        page_extension = MetaTagPageExtension(extended_object=self.page, robots_indexing=True, robots_following=True)
        page_extension.save()
        self.page.publish('en')
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="robots"]').attr('content'), 'noindex, nofollow')

    @override_settings(META_TAGGER_ROBOTS_DOMAIN_WHITELIST=['testserver'])
    def test_robots_are_active(self):
        page_extension = MetaTagPageExtension(extended_object=self.page, robots_indexing=True, robots_following=True)
        page_extension.save()
        self.page.publish('en')
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="robots"]').attr('content'), 'index, follow')

    @override_settings(META_TAGGER_ROBOTS_DOMAIN_WHITELIST=['testserver'])
    def test_robots_are_inactive(self):
        page_extension = MetaTagPageExtension(extended_object=self.page, robots_indexing=False, robots_following=False)
        page_extension.save()
        self.page.publish('en')
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="robots"]').attr('content'), 'noindex, nofollow')

    def test_open_graph_title(self):
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[property="og:title"]').attr('content'), self.page_title)

    def test_open_graph_description(self):
        response = self.client.get('/')
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[property="og:description"]').attr('content'), self.page_description)


class ModelMetaTagTests(MetaTaggerViewTestMixin):
    def setUp(self):
        super(ModelMetaTagTests, self).setUp()
        self._register_apphook()

    def test_instance_title(self):
        news_article = NewsArticle.objects.create(title='My title', meta_title='My meta title')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('title')[0].text, news_article.meta_title)

    def test_page_fallback_if_no_instance_meta_title(self):
        news_article = NewsArticle.objects.create(title='My title', meta_title='')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('title')[0].text, self.page_title)

    def test_instance_description(self):
        news_article = NewsArticle.objects.create(title='My title', meta_description='My meta description')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="description"]').attr('content'), news_article.meta_description)

    def test_page_fallback_if_no_instance_meta_description(self):
        news_article = NewsArticle.objects.create(title='My title', meta_description='')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="description"]').attr('content'), self.page_description)

    def test_robots_are_inactive_without_whitelist(self):
        news_article = NewsArticle.objects.create(title='My title', robots_indexing=True, robots_following=True)
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="robots"]').attr('content'), 'noindex, nofollow')

    @override_settings(META_TAGGER_ROBOTS_DOMAIN_WHITELIST=['testserver'])
    def test_robots_are_active(self):
        news_article = NewsArticle.objects.create(title='My title', robots_indexing=True, robots_following=True)
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="robots"]').attr('content'), 'index, follow')

    @override_settings(META_TAGGER_ROBOTS_DOMAIN_WHITELIST=['testserver'])
    def test_robots_are_inactive(self):
        news_article = NewsArticle.objects.create(title='My title', robots_indexing=False, robots_following=False)
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[name="robots"]').attr('content'), 'noindex, nofollow')


class ModelOpenGraphMetaTagTests(MetaTaggerViewTestMixin):
    def setUp(self):
        super(ModelOpenGraphMetaTagTests, self).setUp()
        self._register_apphook()

    def test_open_graph_title(self):
        news_article = NewsArticle.objects.create(title='My title', meta_title='My meta title')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[property="og:title"]').attr('content'), news_article.meta_title)

    def test_page_fallback_if_no_instance_meta_title(self):
        news_article = NewsArticle.objects.create(title='My title', meta_title='')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[property="og:title"]').attr('content'), self.page_title)

    def test_open_graph_description(self):
        news_article = NewsArticle.objects.create(title='My title', meta_description='My meta description')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[property="og:description"]').attr('content'), news_article.meta_description)

    def test_page_fallback_if_no_instance_meta_description(self):
        news_article = NewsArticle.objects.create(title='My title', meta_description='')
        response = self.client.get(reverse('news-article-detail', kwargs={'pk': news_article.pk}))
        content = PyQuery(response.content)
        self.assertEqual(content.find('meta[property="og:description"]').attr('content'), self.page_description)
