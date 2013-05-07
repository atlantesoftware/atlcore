#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components import Component

class JCarousel(Component):
    
    def __init__(self, data_provider=None, version=None):
        super(JCarousel, self).__init__(data_provider, version)
        self._theme = 'tango'
        self._theme_url = ''
        self._librarylist += [{'lib_jquery' : atlcore_settings.JSLIBRARY['lib_jquery']}]
        self._librarylist += [{'lib_jquery.jcarousel' : atlcore_settings.JSLIBRARY['lib_jquery.jcarousel']}]
        
    def __get_theme_url(self):
        if self._theme_url == '':
            return '%scommon/js/jquery.plugins/jcarousel/themes/%s/skin.css' % (atlcore_settings.MEDIA_URL, self._theme)
        else:
            return self._theme_url
    def __set_theme_url(self, value): self._theme_url = str(value)
    theme_url = property(__get_theme_url, __set_theme_url)