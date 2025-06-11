from cms.sitemaps import CMSSitemap


class MetaTagRobotsSiteMap(CMSSitemap):
    def items(self):
        return super().items().exclude(page__metatagpageextension__robots_indexing=False)
