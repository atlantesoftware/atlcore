#encoding=UTF-8
from atlcore.vcl.components.list import List
from atlcore import settings as atlcore_settings

class Carousel(List):
    
    def __init__(self, source = None, driver=None):
        self._html_id = None
        super(Carousel, self).__init__(source, driver)
        self.librarylist += [{'lib_jquery' : atlcore_settings.JSLIBRARY['lib_jquery']}]
        self.librarylist += [{'lib_jquery.carousel' : atlcore_settings.JSLIBRARY['lib_jquery.carousel']}]
        self._theme = '/atlante_core_media/common/js/jquery.plugins/jquerytool/css/themes/default/style.css'
        
                
    def __get_html_id(self):
        if not self._html_id:
            return "carousel"
        else:
            return self._html_id
        
    def __set_html_id(self, value):
        self._html_id = value

    html_id = property(__get_html_id, __set_html_id, 'ID que se le asociará al Carousel')                