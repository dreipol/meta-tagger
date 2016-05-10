from django import template

from meta_tagger.models import MetaTagPageExtension

from ..conf import settings

register = template.Library()


@register.simple_tag
def render_global_meta_tag(tag_name, is_og=False):
    setting_key = 'META_{}'.format(tag_name.upper())

    try:
        # Try to get the settings from constance.
        from constance import config as meta_tag_config
        content = getattr(meta_tag_config, setting_key)
    except ImportError:
        # If constance is not installed, we use the settings in conf.py as fallback.
        meta_tag_config = settings.META_TAGGER_META_TAG_CONF
        content = meta_tag_config.get(setting_key)

    if content:
        return '<meta {attr_name}="{tag_name}" content="{content}">'.format(
            attr_name='name' if not is_og else 'property',
            tag_name=tag_name if not is_og else 'og:{}'.format(tag_name),
            content=content
        )
    return ''


@register.simple_tag(takes_context=True)
def render_title_tag(context, is_og=False):
    """
    Returns the title as string or a complete open graph meta tag.
    """
    request = context['request']
    content = ''

    # Try to get the title from the context object (e.g. DetailViews).
    if context.get('object'):
        content = getattr(context['object'], 'meta_title', None)

    if not content:
        # Try to get the title from the cms page.
        try:
            content = request.current_page.get_page_title()  # Try the `page_title` before the `title of the CMS page.
            if not content:
                content = request.current_page.get_title()
        except AttributeError:
            pass

    if not is_og:
        return content
    else:
        return '<meta property="og:title" content="{content}">'.format(content=content)


@register.simple_tag(takes_context=True)
def render_description_meta_tag(context, is_og=False):
    """
    Returns the description as meta or open graph tag.
    """
    request = context['request']
    content = ''

    # Try to get the description from the context object (e.g. DetailViews).
    if context.get('object'):
        content = getattr(context['object'], 'meta_description', None)

    if not content:
        try:
            # Try for the meta description of the cms page.
            content = request.current_page.get_meta_description()
        except AttributeError:
            pass

    if content:
        return '<meta {attr_name}="{tag_name}" content="{content}">'.format(
            attr_name='name' if not is_og else 'property',
            tag_name='description' if not is_og else 'og:description',
            content=content
        )
    else:
        return ''


@register.simple_tag(takes_context=True)
def render_robots_meta_tag(context):
    """
    Returns the robots meta tag.
    """
    request = context['request']
    robots_indexing = False
    robots_following = False

    if not settings.DEBUG:
        try:
            # Try to get the description from the context object (e.g. DetailView).
            robots_indexing = getattr(context['object'], 'robots_indexing', None)
            robots_following = getattr(context['object'], 'robots_following', None)
        except KeyError:
            try:
                # Try fetching the robots values of the cms page.
                robots_indexing = request.current_page.metatagpageextension.robots_indexing
                robots_following = request.current_page.metatagpageextension.robots_following
            except MetaTagPageExtension.DoesNotExist:
                pass

    return '<meta name="robots" content="{robots_indexing}, {robots_following}">'.format(
        robots_indexing='index' if robots_indexing else 'noindex',
        robots_following='follow' if robots_following else 'nofollow'
    )


@register.simple_tag(takes_context=True)
def render_image_meta_tag(context):
    request = context['request']
    og_image = None

    # Try to get the image from the context object (e.g. DetailView).
    if context.get('object'):
        og_image = getattr(context['object'], 'og_image', None)

    if not og_image:
        try:
            # Try fetching the image of the cms page.
            og_image = request.current_page.metatagpageextension.og_image
        except MetaTagPageExtension.DoesNotExist:
            pass

    if og_image:
        return '<meta property="og:image" content="{content}">'.format(content=og_image.file.url)
    else:
        return ''
