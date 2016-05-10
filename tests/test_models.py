#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cms.api import create_page
from django.test import TestCase

from meta_tagger.models import MetaTagPageExtension


class MetaTagPageExtensionTests(TestCase):
    def test_meta_tag_page_extension(self):
        page = create_page('Test Page Extension', 'meta_tagger/index.html', 'en')
        page_extension = MetaTagPageExtension(extended_object=page, robots_indexing=True, robots_following=False)
        page_extension.save()

        page.metatagpageextension = page_extension
        page.publish('en')

        self.assertTrue(page_extension.robots_indexing)
        self.assertEqual(page_extension.robots_indexing, page.publisher_public.metatagpageextension.robots_indexing)
        self.assertFalse(page_extension.robots_following)
        self.assertEqual(page_extension.robots_following, page.publisher_public.metatagpageextension.robots_following)
