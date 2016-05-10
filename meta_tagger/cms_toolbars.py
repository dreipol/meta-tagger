from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from django.utils.translation import ugettext_lazy as _

from .models import MetaTagPageExtension


@toolbar_pool.register
class MetaTagPageExtensionToolbar(ExtensionToolbar):
    model = MetaTagPageExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()

        if current_page_menu:
            page_extension, url = self.get_page_extension_admin()

            if url:
                current_page_menu.add_modal_item(_('Meta Tags'), url=url, disabled=not self.toolbar.edit_mode)
