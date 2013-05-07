#encoding=UTF-8

from atlcore import settings as atlcore_settings
from django.conf import settings
from atlcore.vcl.components.component import Component
from atlcore.contenttype.models import Video
        
class JWPlayer(Component):
    
    def __init__(self, data_provider=None):
        super(JWPlayer, self).__init__(data_provider)
        #self.version = '5.1.854'
        self._template['default'] = 'vcl/jwplayer.html'
        self.flashplayer = '%scommon/jwplayer/jwplayer_v5_8/player.swf ' % settings.STATIC_URL
        if isinstance(data_provider, Video):
            if data_provider.video_source == 'embeded':
                self.embed = data_provider.embeded_video
            elif data_provider.video_source == 'external':
                self.file = data_provider.external_url
                # adjust for vimeo videos
                if self.file.find('http://vimeo.com') > -1:
                    self.type = '%scommon/jwplayer/jwplayer_v5_8/vimeo.swf' % settings.STATIC_URL
            else:                    
                self.file = '%s%s' % (settings.STATIC_URL, data_provider.video)
                self.image = '%s%s' % (settings.STATIC_URL, data_provider.thumbnail)
        self.width = 480
        self.height = 270
        self.autostart = False
        self.controlbar = 'bottom'
        self.flashplayer = '%scommon/jwplayer/jwplayer_v5_8/player.swf' % settings.STATIC_URL
        self.skin = '%scommon/jwplayer/jwplayer_v5_8/skins/beelden/beelden.zip' % settings.STATIC_URL
        self._librarylist += [{'lib_jquery' : atlcore_settings.JSLIBRARY['lib_jquery']}]
        self._librarylist += [{'lib_jwplayer_v5_8' : atlcore_settings.JSLIBRARY['lib_jwplayer_v5_8']}]


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

