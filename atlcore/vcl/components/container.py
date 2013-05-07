#encoding=UTF-8
from atlcore.vcl.components.component import Component
from atlcore.vcl.exceptions import ComponentVersionError
from atlcore.settings import MEDIA_URL as ATL_MEDIA_URL

class Container(Component):
    
    def __init__(self, data_provider,  version=None):
        super(Container, self).__init__(data_provider, version)
        self.id = data_provider.id
        self._template['default']= 'vcl/content/content_details.html'
        self._template['details']= 'vcl/content/container_details.html' #% data_provider.class_name_instance
        self._template['preview']= 'vcl/content/container_preview.html' #% data_provider.class_name_instance
        
        #self._librarylist += [{'lib_container' : '%s/vcl/js/container.js' % ATL_MEDIA_URL}]
        
