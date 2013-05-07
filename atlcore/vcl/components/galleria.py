#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component
from atlcore.settings import MEDIA_URL, JSLIBRARY

class Galleria(Component):
    
    def __init__(self, data_provider=None, version=None):
        super(Galleria, self).__init__(data_provider, version)
        self._theme = 'classic'
        self._theme_url = ''
        self._theme_script_url = ''
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._librarylist += [{'lib_galleria': JSLIBRARY['lib_galleria']}]
        self._stylelist += [{'galleria_style': '%svcl/css/galleria.css' % MEDIA_URL}]
    
    def __get_theme_url(self):
        if self._theme_url == '':
            return '%scommon/js/jquery.plugins/galleria/themes/%s/galleria.%s.css' % (atlcore_settings.MEDIA_URL, self._theme, self._theme)
        else:
            return self._theme_url
    def __set_theme_url(self, value): self._theme_url = str(value)
    theme_url = property(__get_theme_url, __set_theme_url)
    
    def __get_theme_script_url(self):
        if self._theme_script_url == '':
            return '%scommon/js/jquery.plugins/galleria/themes/%s/galleria.%s.min.js' % (atlcore_settings.MEDIA_URL, self._theme, self._theme)
        else:
            return self._theme_script_url
    def __set_theme_script_url(self, value): self._theme_script_url = str(value)
    theme_script_url = property(__get_theme_script_url, __set_theme_script_url)