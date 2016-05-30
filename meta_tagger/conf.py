from appconf import AppConf
from django.conf import settings  # noqa


class MyAppConf(AppConf):
    META_TAG_CONF = {
        'META_AUTHOR': '',
        'META_PUBLISHER': '',
        'META_COPYRIGHT': '',
        'META_COMPANY': '',
        'META_SITE_NAME': '',
        'META_TYPE': '',
        'META_OG_IMAGE_WIDTH': 1200,
        'META_OG_IMAGE_HEIGHT': 630,
    }

    ROBOTS_DOMAIN_WHITELIST = []
