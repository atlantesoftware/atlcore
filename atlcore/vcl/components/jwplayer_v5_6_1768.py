#encoding=UTF-8

from atlcore import settings as atlcore_settings
from django.conf import settings
from atlcore.vcl.components.component import Component
        
class JWPlayer(Component):
    
    def __init__(self, source=None, driver=None):
        super(JWPlayer, self).__init__(source, driver)
        self.version = '5.6.1768'
        self.template['default'] = 'vcl/jwplayer.html'
        #self._config['skin'] = '%scommon/swf/stylish.swf ' % atlcore_settings.MEDIA_URL
        self._config['file'] = ''
        self._config['image'] = ''
        self._config['width'] = 480
        self._config['height'] = 270
        self._config['autostart'] = False
        self._config['flashplayer'] = '%scommon/jwplayer/jwplayer_v5_6_1768/player.swf' % (atlcore_settings.MEDIA_URL)
        self.librarylist += [{'lib_jquery' : atlcore_settings.JSLIBRARY['lib_jquery']}]
        self.librarylist += [{'lib_jwplayer_v5_6_1768' : atlcore_settings.JSLIBRARY['lib_jwplayer_v5_6_1768']}]
        
    def __get_plugins(self): return self._config['plugins']
    def __set_plugins(self, value): self._config['plugins'] = value
    plugins = property(__get_plugins, __set_plugins)
    
    
    def __get_file(self): return self._config['file']
    def __set_file(self, value): self._config['file'] = value
    file = property(__get_file, __set_file)
    
    def __get_image(self): return self._config['image']
    def __set_image(self, value): self._config['image'] = value
    image = property(__get_image, __set_image)
    
    def __get_autostart(self): return self._config['autostart']
    def __set_autostart(self, value): self._config['autostart'] = value
    autostart = property(__get_autostart, __set_autostart)
    
    def __get_skin(self): return self._config['skin']
    def __set_skin(self, value): self._config['skin'] = value
    skin = property(__get_skin, __set_skin)
    
    def __get_width(self): return self._config['width']
    def __set_width(self, value): self._config['width'] = value
    width = property(__get_width, __set_width)
    
    def __get_height(self): return self._config['height']
    def __set_height(self, value): self._config['height'] = value
    height = property(__get_height, __set_height)

    def setWidth(self, width):
        if self.data_provider.x_aspect_ratio and self.data_provider.y_aspect_ratio:
            self.height = width * (self.data_provider.y_aspect_ratio /self.data_provider.x_aspect_ratio )
            self.width = width
        else:
            self.height = width * (float(9) /float(16) )
            self.width = width
    
    def setHeight(self, height):
        if self.data_provider.x_aspect_ratio and self.data_provider.y_aspect_ratio:
            self.width = height * (self.data_provider.x_aspect_ratio /self.data_provider.y_aspect_ratio )
            self.height = height
        else:
            self.width = height * (float(16) /float(9) ) 
            self.height = height

