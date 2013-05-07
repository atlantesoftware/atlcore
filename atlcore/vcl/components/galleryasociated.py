#encoding=UTF-8
from atlcore.vcl.components.component import Component
from django.conf import settings
from atlcore.settings import JSLIBRARY
from siteapp.controller import ControlLogic
from atlcore.contenttype.models.content import Content
from atlcore.base_conf import MEDIA_URL as BASE_MEDIA_URL



class GalleryAsociated(Component):
    
    def __init__(self, id , data_provider=None, cant = 1, width = 128, height = 128, exclude = None, url = None, version=None):
        super(GalleryAsociated, self).__init__(data_provider, version)
        self.id = id
        self.items = data_provider
        self.url = url
        self.cant = cant
        self.width = width
        self.height = height
        self.exclude = exclude
        self.stylelist += [{"galleryasociated": "%svcl/galleryasociated/css/galleryasociated.css" % BASE_MEDIA_URL}]
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]


class Gallery(Component):
    
    def __init__(self, id , data_provider=None, cant = 1, width = 128, height = 128, url = None, version=None):
        super(Gallery, self).__init__(data_provider, version)
        self.id = id
        self.items = data_provider
        self.url = url
        self.cant = cant
        self.width = width
        self.height = height
        self.stylelist += [{"gallery": "%svcl/gallery/css/gallery.css" % settings.MEDIA_URL}]
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]


class GalleryColumnRight(Component):
    
    def __init__(self, id , data_provider=None, cant = 1, width = 128, height = 128, url = None, version=None):
        super(GalleryColumnRight, self).__init__(data_provider, version)
        self.id = id
        self.items = data_provider
        self.url = url
        self.cant = cant
        self.width = width
        self.height = height
        self.stylelist += [{"galleryasociated": "%svcl/galleryasociated/css/gallerycolumnright.css" % settings.MEDIA_URL}]
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]

