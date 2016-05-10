from cms.sitemaps import CMSSitemap


class MetaTagRobotsSiteMap(CMSSitemap):
    def items(self):
        return super(MetaTagRobotsSiteMap, self).items().exclude(page__metatagpageextension__robots_indexing=False)
