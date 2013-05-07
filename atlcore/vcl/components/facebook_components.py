#encoding=UTF-8
from atlcore.vcl.components import Component
from atlcore import settings as atlcore_settings


class FacebookLikeButton(Component):
    
    def __init__(self, href=None, width = 300, send = False, faces = False):
        super(FacebookLikeButton, self).__init__()
        self.href = href
        self.width = width
        self.send = send
        self.faces = faces 
        
        self._librarylist += [{'lib_facebook_plugins' : atlcore_settings.JSLIBRARY['lib_facebook_plugins']}]
    
    def __get_href(self): return self._href
    def __set_href(self, value): self._href = value
    href = property(__get_href,__set_href)


class FacebookLikeBox(Component):
    
    def __init__(self, href=None, width = 300, height = 292, send = False, faces = False):
        super(FacebookLikeBox, self).__init__()
        self.href = href
        self.width = width
        self.height = height
        self.send = send
        self.faces = faces
        
        self._librarylist += [{'lib_facebook_plugins' : atlcore_settings.JSLIBRARY['lib_facebook_plugins']}]
    
    def __get_href(self): return self._href
    def __set_href(self, value): self._href = value
    href = property(__get_href,__set_href)

class FacebookLike(Component):
    
    def __init__(self, href=None, width = 300, height = 292, send = False, faces = False, colorscheme="light"):
        super(FacebookLike, self).__init__()
        self.href = href
        self.width = width
        self.height = height
        self.send = send
        self.faces = faces
        self.colorscheme = colorscheme
        
        self._librarylist += [{'lib_facebook_plugins' : atlcore_settings.JSLIBRARY['lib_facebook_plugins']}]
    
    def __get_href(self): return self._href
    def __set_href(self, value): self._href = value
    href = property(__get_href,__set_href)


class FacebookRecommendations(Component):
    
    def __init__(self, site=None, width = 300, height = 292):
        super(FacebookRecommendations, self).__init__()
        self.site = site
        self.width = width
        self.height = height
        self._librarylist += [{'lib_facebook_plugins' : atlcore_settings.JSLIBRARY['lib_facebook_plugins']}]


class FacebookActivity(Component):
    
    def __init__(self, site=None, width = 300, height = 292):
        super(FacebookActivity, self).__init__()
        self.site = site
        self.width = width
        self.height = height
        self._librarylist += [{'lib_facebook_plugins' : atlcore_settings.JSLIBRARY['lib_facebook_plugins']}]

