from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class AtlContentType(CMSApp):
    name = _("AtlContentType")
    urls = ['atlcore.contenttype.urls']

apphook_pool.register(AtlContentType)