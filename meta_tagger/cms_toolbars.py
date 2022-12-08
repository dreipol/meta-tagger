from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from django.utils.translation import gettext_lazy as _
from pkg_resources import get_distribution, parse_version

from .models import MetaTagPageExtension


@toolbar_pool.register
class MetaTagPageExtensionToolbar(ExtensionToolbar):
    model = MetaTagPageExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()

        if current_page_menu:
            page_extension, url = self.get_page_extension_admin()

            if url:
                if parse_version(get_distribution('django-cms').version) >= parse_version('3.6.0'):
                    disabled = not self.toolbar.edit_mode_active
                else:
                    disabled = not self.toolbar.edit_mode

                current_page_menu.add_modal_item(_('Meta Tags'), url=url, disabled=disabled)
