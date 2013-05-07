#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component

class ToolBar(Component):
    
    def __init__(self, source=None, driver=None):
        super(ToolBar, self).__init__(source, driver)
        self._button_list = []
        
    def __get_button_list(self): return self._button_list
    def __set_button_list(self, value): self._button_list = value
    button_list = property(__get_button_list, __set_button_list)