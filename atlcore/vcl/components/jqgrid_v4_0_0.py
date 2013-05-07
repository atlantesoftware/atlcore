#encoding=UTF-8
from atlcore.settings import JSLIBRARY, MEDIA_URL
from atlcore.vcl.components import Component

class JQGrid_v4_0_0(Component):
    
    def __init__(self, data_provider):
        super(JQGrid_v4_0_0, self).__init__(data_provider)
        self.colNames = data_provider.colnames
        self.colModel = []
        for col in self.colNames:
            self.colModel.append({'name': col, 'index': col, 'width':50})
        self.pager = '#pager'
        self.url = str(data_provider.url)
        self.datatype = 'JSON'
        self.editurl = data_provider.editurl
        self.onSelectRow = ''
        self.multiselect = 0
        self._theme = 'atlcms'
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        #self.librarylist += [{'lib_jquery.layout' : JSLIBRARY['lib_jquery.layout']}]
        self._librarylist += [{'lib_jquery.ui.core' : JSLIBRARY['lib_jquery.ui.core']}]
        self._librarylist += [{'lib_jquery.ui.widget' : JSLIBRARY['lib_jquery.ui.widget']}]
        self._librarylist += [{'lib_jquery.ui.button' : JSLIBRARY['lib_jquery.ui.button']}]
        self._librarylist += [{'lib_jquery.ui.mouse' : JSLIBRARY['lib_jquery.ui.mouse']}]
        self._librarylist += [{'lib_jquery.ui.sortable' : JSLIBRARY['lib_jquery.ui.sortable']}]
        self._librarylist += [{'lib_jquery.ui.droppable' : JSLIBRARY['lib_jquery.ui.droppable']}]
        self._librarylist += [{'lib_jquery.ui.draggable' : JSLIBRARY['lib_jquery.ui.draggable']}]
        self._librarylist += [{'lib_grid.locale-es' : JSLIBRARY['lib_grid.locale-es']}]
        self._librarylist += [{'lib_jquery.jqgrid_v4_0_0' : JSLIBRARY['lib_jquery.jqgrid_v4_0_0']}]
        self._librarylist += [{'lib_jquery.jquery.tablednd' : JSLIBRARY['lib_jquery.jquery.tablednd']}]
        self._librarylist += [{'lib_jquery.jquery.contextmenu' : JSLIBRARY['lib_jquery.jquery.contextmenu']}]
        self._librarylist += [{'lib_jquery.ui.multiselect' : JSLIBRARY['lib_jquery.ui.multiselect']}]
        #self.stylelist += [{'css_jquery-ui' : '%s/common/js/jquery.plugins/jqgrid/css/redmond/jquery-ui-1.8.2.custom.css' % MEDIA_URL}]
        self._stylelist += [{'css_theme-%s' % self._theme : '/common/jquery/ui/v1.8.13/themes/%s/jquery.ui.all.css' % self._theme}]
        self._stylelist += [{'css_jqgrid' : '/common/js/jquery.plugins/jqgrid/css/ui.jqgrid.css'}]
        self._stylelist += [{'css_jqgrid' : '/common/jquery/plugins/jqgrid/jqgrid_v4_0_0/plugins/ui.multiselect.css'}]
