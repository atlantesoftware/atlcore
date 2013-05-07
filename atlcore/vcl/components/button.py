#encoding=UTF-8
from atlcore.settings import JSLIBRARY, MEDIA_URL
from atlcore.vcl.components import Component

class Button(Component):
    
    def __init__(self, data_provider=None, version=None):
        super(Button, self).__init__(data_provider, version)
        self.disabled = False
        self.text = True
        self.icons = {'primary': None, 'secondary': None}
        self.label = 'button'
        self._theme = 'base'
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._librarylist += [{'lib_jquery.ui.core' : JSLIBRARY['lib_jquery.ui.core']}]
        self._librarylist += [{'lib_jquery.ui.widget' : JSLIBRARY['lib_jquery.ui.widget']}]
        self._librarylist += [{'lib_jquery.ui.button' : JSLIBRARY['lib_jquery.ui.button']}]
        self._stylelist += [{'css_theme-%s' % self._theme : '/common/jquery/ui/v1.8.13/themes/%s/jquery.ui.all.css' % self._theme}]
            
    def __get_theme(self): return self._theme
    def __set_theme(self, value):
        self._stylelist.remove({'css_theme-%s' % self._theme : '/common/jquery/ui/v1.8.13/themes/%s/jquery.ui.all.css' % self._theme})
        self._stylelist += [{'css_theme-%s' % str(value) : '/common/jquery/ui/v1.8.13/themes/%s/jquery.ui.all.css' % str(value)}] 
        self._theme = str(value)
    theme = property(__get_theme, __set_theme, "Skin que se usará para mostrar el objeto")
    