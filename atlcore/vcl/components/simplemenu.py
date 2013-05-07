#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component
from atlcore.settings import MEDIA_URL

class MenuItem(object):
    pass

class SimpleMenu(Component):
    
    def __init__(self, data_provider=None, version=None):
        super(SimpleMenu, self).__init__(data_provider, version)
        self.items = data_provider
        self.separator = None
        self._stylelist += [{'simple_menu': '%svcl/css/simple_menu.css' % MEDIA_URL}]
    
    