from contextlib import suppress

from cms.models import Title
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from meta_tagger.models import MetaTagPageExtension


class RobotsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'pages': self.get_pages(),
            'sitemap_url': self.get_sitemap_url()
        }
        return render(request, 'robots.txt', context, content_type='text/plain')

    @staticmethod
    def get_page_title_queryset():
        return Title.objects.public().filter(
            Q(redirect='') | Q(redirect__isnull=True),
            page__login_required=False,
            page__site=Site.objects.get_current(),
        ).order_by('page__path')

    def get_pages(self) -> list:
        pages = []
        for title in self.get_page_title_queryset():
            with suppress(MetaTagPageExtension.DoesNotExist):
                if title.page.metatagpageextension.robots_disallow:
                    pages.append({
                        'instruction': 'Disallow',
                        'path': title.page.get_absolute_url(title.language)
                    })
        return pages

    def get_sitemap_url(self) -> str:
        scheme = 'https' if self.request.is_secure() else 'http'
        site = get_current_site(self.request)
        path = reverse('sitemap')
        return '{scheme}://{site}{path}'.format(scheme=scheme, site=site, path=path)
