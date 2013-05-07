#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component
from atlcore.settings import MEDIA_URL, JSLIBRARY

class MenuItem(object):
    pass

class ContentList(Component):
    
    def __init__(self, data_provider=None, version=None):
        super(ContentList, self).__init__(data_provider, version)
        self.items = data_provider
        self._stylelist += [{'two_level_menu': '%svcl/css/contentlist.css' % MEDIA_URL}]
    
    