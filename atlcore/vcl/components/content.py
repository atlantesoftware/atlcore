#encoding=UTF-8
from atlcore.vcl.components.component import Component
from atlcore.vcl.exceptions import ComponentVersionError
from atlcore.settings import MEDIA_URL as ATL_MEDIA_URL
from atlcore.contenttype.models import Container

class Content(Component):
    
    def __init__(self, data_provider,  version=None):
        super(Content, self).__init__(data_provider, version)
        self.id = data_provider.id
        self._template['default']= 'vcl/content/content_details.html'
        self._template['details']= 'vcl/content/%s_details.html' % data_provider.class_name_instance
        self._template['preview']= 'vcl/content/%s_preview.html' % data_provider.class_name_instance
        if isinstance(data_provider, Container):
            self._template['thumbnails']= 'vcl/content/container_thumbnails.html'
        
