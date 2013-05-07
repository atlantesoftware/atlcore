#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component
from atlcore.settings import MEDIA_URL, JSLIBRARY

class Galleriffic(Component):
    
    def __init__(self, data_provider=None, version=None):
        super(Galleriffic, self).__init__(data_provider, version)
        self._theme = 'classic'
        self._theme_url = ''
        self._theme_script_url = ''
        
        self.imageContainerSel = '#slideshow'
        self.controlsContainerSel = '#controls'
        self.captionContainerSel = '#caption'
        self.loadingContainerSel = '#loading'
        self.renderNavControls = True
        
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._librarylist += [{'lib_jquery.history': JSLIBRARY['lib_jquery.history']}]
        self._librarylist += [{'lib_galleriffic': JSLIBRARY['lib_galleriffic']}]
        self._librarylist += [{'lib_jquery.opacityrollover': JSLIBRARY['lib_jquery.opacityrollover']}]

        self._stylelist += [{'style_galleriffic3_basic': '%scommon/js/jquery.plugins/galleriffic/css/basic.css' % atlcore_settings.MEDIA_URL}]
        self._stylelist += [{'style_galleriffic3': '%scommon/js/jquery.plugins/galleriffic/css/galleriffic-3.css' % atlcore_settings.MEDIA_URL}]
