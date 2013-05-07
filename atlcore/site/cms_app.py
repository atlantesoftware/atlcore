from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MyApphook(CMSApp):
    name = _("My Apphook")
    urls = ['atlcore.site.urls_new']

#apphook_pool.register(MyApphook)