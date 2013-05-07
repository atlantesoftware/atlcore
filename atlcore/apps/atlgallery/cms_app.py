__author__ = 'hailem'

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class AtlGallery(CMSApp):
    name = _("Atlante Gallery")
    urls = ['atlgallery.urls']

apphook_pool.register(AtlGallery)