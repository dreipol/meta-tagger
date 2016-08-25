from django import template
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer

from meta_tagger.helpers import get_setting_variable
from meta_tagger.models import MetaTagPageExtension

from ..conf import settings

register = template.Library()


@register.simple_tag
def render_global_meta_tag(tag_name, is_og=False):
    content = get_setting_variable(name='META_{}'.format(tag_name.upper()))

    if content:
        return mark_safe('<meta {attr_name}="{tag_name}" content="{content}">'.format(
            attr_name='name' if not is_og else 'property',
            tag_name=tag_name if not is_og else 'og:{}'.format(tag_name),
            content=content
        ))
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
        try:
            content = context['object'].get_meta_title()
        except AttributeError:
            pass

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
        return mark_safe('<meta property="og:title" content="{content}">'.format(content=content))


@register.simple_tag(takes_context=True)
def render_description_meta_tag(context, is_og=False):
    """
    Returns the description as meta or open graph tag.
    """
    request = context['request']
    content = ''

    # Try to get the description from the context object (e.g. DetailViews).
    if context.get('object'):
        try:
            content = context['object'].get_meta_description()
        except AttributeError:
            pass

    if not content:
        try:
            # Try for the meta description of the cms page.
            content = request.current_page.get_meta_description()
        except AttributeError:
            pass

    if content:
        return mark_safe('<meta {attr_name}="{tag_name}" content="{content}">'.format(
            attr_name='name' if not is_og else 'property',
            tag_name='description' if not is_og else 'og:description',
            content=content
        ))
    else:
        return ''


@register.simple_tag(takes_context=True)
def render_robots_meta_tag(context):
    """
    Returns the robots meta tag.
    """
    request = context['request']
    robots_indexing = None
    robots_following = None

    # Prevent indexing any unwanted domains (e.g. staging).
    if context.request.get_host() in settings.META_TAGGER_ROBOTS_DOMAIN_WHITELIST:

        # Try to get the title from the context object (e.g. DetailViews).
        if context.get('object'):
            try:
                robots_indexing = context['object'].get_robots_indexing()
                robots_following = context['object'].get_robots_following()
            except AttributeError:
                pass

        try:
            # Try fetching the robots values of the cms page.
            if robots_indexing is None:
                robots_indexing = request.current_page.metatagpageextension.robots_indexing
            if robots_following is None:
                robots_following = request.current_page.metatagpageextension.robots_following
        except (AttributeError, MetaTagPageExtension.DoesNotExist):
            pass

    return mark_safe('<meta name="robots" content="{robots_indexing}, {robots_following}">'.format(
        robots_indexing='index' if robots_indexing else 'noindex',
        robots_following='follow' if robots_following else 'nofollow'
    ))


@register.simple_tag(takes_context=True)
def render_image_meta_tag(context):
    request = context['request']
    og_image = None
    og_image_width = None
    og_image_height = None

    # Try to get the image from the context object (e.g. DetailView).
    if context.get('object'):
        try:
            og_image = context['object'].get_og_image()
            og_image_width = context['object'].get_og_image_width()
            og_image_height = context['object'].get_og_image_height()
        except AttributeError:
            pass

    if not og_image:
        try:
            # Try fetching the image of the cms page.
            og_image = request.current_page.metatagpageextension.og_image
        except (AttributeError, MetaTagPageExtension.DoesNotExist):
            pass

    if og_image:

        if not og_image_width:
            try:
                # Try fetching the image width of the cms page.
                og_image_width = request.current_page.metatagpageextension.og_image_width
            except (AttributeError, MetaTagPageExtension.DoesNotExist):
                pass

            if not og_image_width:
                # Use the default from the settings.
                og_image_width = get_setting_variable(name='META_OG_IMAGE_WIDTH')

        if not og_image_height:
            try:
                # Try fetching the image height of the cms page.
                og_image_height = request.current_page.metatagpageextension.og_image_height
            except (AttributeError, MetaTagPageExtension.DoesNotExist):
                pass

            if not og_image_height:
                # Use the default from the settings.
                og_image_height = get_setting_variable(name='META_OG_IMAGE_HEIGHT')

        # Create a thumbnail to get the absolute url.
        thumbnailer_options = {'size': (og_image_width, og_image_height), 'crop': True}
        thumbnail = get_thumbnailer(og_image).get_thumbnail(thumbnailer_options)

        # Depending on the storage backend we have to prefix the url with the scheme and the host.
        if thumbnail.url[:4] == 'http':
            url = thumbnail.url
        else:
            url = '{scheme}://{host}{path}'.format(scheme=context.request.scheme, host=context.request.get_host(),
                                                   path=thumbnail.url)

        image_tag = '<meta property="og:image" content="{content}">'.format(content=url)
        width_tag = '<meta property="og:image:width" content="{content}">'.format(content=og_image_width)
        height_tag = '<meta property="og:image:height" content="{content}">'.format(content=og_image_height)
        return mark_safe(image_tag + width_tag + height_tag)

    else:
        return ''
