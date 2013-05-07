#encoding=UTF-8
from atlcore.vcl.components import Component
from atlcore import settings as atlcore_settings

class Search(Component):
    
    def __init__(self, page=None, title = None):
        super(Search, self).__init__()
        self.page = page
        self.title = title
        
        self._librarylist += [{'lib_facebook_plugins' : atlcore_settings.JSLIBRARY['lib_facebook_plugins']}]
    
    def __get_href(self): return self._href
    def __set_href(self, value): self._href = value
    href = property(__get_href,__set_href)