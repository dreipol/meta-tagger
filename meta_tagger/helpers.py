from django.conf import settings


def get_setting_variable(name):
    try:
        # Try to get the settings from constance.
        from constance import config as meta_tag_config
        return getattr(meta_tag_config, name)
    except ImportError:
        # If constance is not installed, we use the settings in conf.py as fallback.
        meta_tag_config = settings.META_TAGGER_META_TAG_CONF
        return meta_tag_config.get(name)
