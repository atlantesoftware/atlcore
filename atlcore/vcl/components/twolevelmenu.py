#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component
from atlcore.settings import MEDIA_URL, JSLIBRARY
from atlcore.contenttype.models import Link

class MenuItem(object):
    
    def __init__(self, id=None, title=None, url=None, selected=None, sub_items=None):
        super(MenuItem, self).__init__()
        self._id = id
        self._title = title
        self._url = url
        self._selected = selected
        self.sub_items = sub_items
        self._image = None
        
    def __get_id(self): return self._id
    def __set_id(self, value): self._id = value
    id = property(__get_id, __set_id)
    
    def __get_title(self): return self._title
    def __set_title(self, value): self._title = value
    title = property(__get_title, __set_title)
    
    def __get_url(self): return self._url
    def __set_url(self, value): self._url = value
    url = property(__get_url, __set_url)

    def __get_image(self): return self._image
    def __set_image(self, value): self._image = value
    image = property(__get_image, __set_image)

    def __get_selected(self): return self._selected
    def __set_selected(self, value): self._selected = value
    selected = property(__get_selected, __set_selected)


class TwoLevelMenu(Component):
    
    def __init__(self, data_provider=None, version=None, request=None):
        super(TwoLevelMenu, self).__init__(data_provider, version)
        self.items = []
        for node in self.data_provider:
            instance = node.get_instance()
            item = MenuItem(id=instance.id, title=instance.title)
            if instance.image:
                item.image = instance.image_absolute_url()
            if instance.instance_class_name == 'folder':
                item.sub_items = []
                subnodes = node.get_instance().get_childrens(type=Link)
                item.url = subnodes[0].get_absolute_url()
                for subnode in subnodes:
                    sub_menu = MenuItem(id=subnode.id, title=subnode.title, url=subnode.url)
                    if request is not None:
                        if subnode.url == request.get_full_path():
                            item.selected = True
                            sub_menu.selected = True
                    item.sub_items.append(sub_menu)
            else:
                item.url = instance.url
                if request is not None:
                    item.selected = (instance.url == request.get_full_path())
            self.items.append(item) 
        self.separator = None
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._stylelist += [{'two_level_menu': '%svcl/twolevelmenu/css/two_level_menu.css' % MEDIA_URL}]
    
    