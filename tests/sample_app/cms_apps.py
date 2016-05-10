from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class SampleApphook(CMSApp):
    name = 'My Sample Apphook'
    urls = ['tests.sample_app.urls']

apphook_pool.register(SampleApphook)
