#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component
from atlcore.settings import MEDIA_URL, JSLIBRARY

class TwoColumnLinkBox(Component):
    
    def __init__(self, data_provider=None, version=None):
        super(TwoColumnLinkBox, self).__init__(data_provider, version)
        self.items = data_provider
        self.column = 2
        if len(data_provider) % self.column > 0:
            self.column_items = (len(data_provider) / self.column) +1
        else:
            self.column_items = len(data_provider) / self.column
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._stylelist += [{'twocolumnlinkbox_styles': '%svcl/twocolumnlinkbox/css/styles.css' % MEDIA_URL}]