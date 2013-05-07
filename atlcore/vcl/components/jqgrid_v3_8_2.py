#encoding=UTF-8
from atlcore import settings as atlcore_settings
from atlcore.vcl.components.component import Component

class JQGrid_v3_8_2(Component):
    
    def __init__(self, source, driver=None):
        super(JQGrid_v3_8_2, self).__init__(source, driver)
        self.datamanager = source
        self._config['url'] = str(self.datamanager.url)
        self._config['datatype'] = 'JSON'
        self._config['mtype'] = 'GET'
        self._config['colNames'] = source.colnames
        self._config['colModel'] = []
        for col in self.colnames:
            self.config['colModel'].append({'name': col, 'index': col, 'width':50})
        self._config['autowidth'] = 'true'
        self._config['pager'] = '#pager'
        self._config['rowNum'] = 10
        self._config['rowList'] = [5,10,20]
        self._config['sortname'] = self.colnames[0]
        self._config['sortorder'] = 'asc'
        self._config['viewrecords'] = 'true'
        self._config['imppath']  = ''
        self._config['caption'] = 'Grid'
        self._config['editurl'] = self.datamanager.editurl
        self._config['toolbar'] = ['false','top']
        self._config['onSelectRow'] = ''
        self.librarylist += [{'lib_jquery' : atlcore_settings.JSLIBRARY['lib_jquery']}]
        self.librarylist += [{'lib_jquery.layout' : atlcore_settings.JSLIBRARY['lib_jquery.layout']}]
        self.librarylist += [{'lib_jquery.ui' : atlcore_settings.JSLIBRARY['lib_jquery.ui']}]
        self.librarylist += [{'lib_jquery.ui.widget' : atlcore_settings.JSLIBRARY['lib_jquery.ui.widget']}]
        self.librarylist += [{'lib_jquery.ui.sortable' : atlcore_settings.JSLIBRARY['lib_jquery.ui.sortable']}]
        self.librarylist += [{'lib_jquery.ui.droppable' : atlcore_settings.JSLIBRARY['lib_jquery.ui.droppable']}]
        self.librarylist += [{'lib_jquery.ui.draggable' : atlcore_settings.JSLIBRARY['lib_jquery.ui.draggable']}]
        self.librarylist += [{'lib_grid.locale-es' : atlcore_settings.JSLIBRARY['lib_grid.locale-es']}]
        self.librarylist += [{'lib_jquery.jqgrid_v3_8_2' : atlcore_settings.JSLIBRARY['lib_jquery.jqgrid_v3_8_2']}]
        #self.stylelist += [{'css_jquery-ui' : '%s/common/js/jquery.plugins/jqgrid/css/redmond/jquery-ui-1.8.2.custom.css' % atlcore_settings.MEDIA_URL}]
        self.stylelist += [{'css_jqgrid' : '%s/common/js/jquery.plugins/jqgrid/css/ui.jqgrid.css' % atlcore_settings.MEDIA_URL}]
        
    def __get_url(self): return self._config['url']
    def __set_url(self, value): self._config['url'] = value
    url = property(__get_url, __set_url)

    def __get_datatype(self): return self._config['datatype']
    def __set_datatype(self, value): self._config['datatype'] = value
    datatype = property(__get_datatype, __set_datatype)

    def __get_colnames(self): return self._config['colNames']
    def __set_colnames(self, value): self._config['colNames'] = value
    colnames = property(__get_colnames, __set_colnames)

    def __get_colmodel(self): return self._config['colModel']
    def __set_colmodel(self, value): self._config['colModel'] = value
    colmodel = property(__get_colmodel, __set_colmodel)
    
    def __get_autowidth(self): return self._config['autowidth']
    def __set_autowidth(self, value): self._config['autowidth'] = value
    autowidth = property(__get_autowidth, __set_autowidth)
    
    def __get_rownum(self): return self._config['rowNum']
    def __set_rownum(self, value): self._config['rowNum'] = value
    rownum = property(__get_rownum, __set_rownum)
    
    def __get_rowlist(self): return self._config['rowList']
    def __set_rowlist(self, value): self._config['rowList'] = value
    rowlist = property(__get_rowlist, __set_rowlist)

    def __get_pager(self): return self._config['pager'][1:len(self._config['pager'])]
    def __set_pager(self, value): self._config['pager'] = '#%s' % value
    pager = property(__get_pager, __set_pager)

    def __get_sortname(self): return self._config['sortname']
    def __set_sortname(self, value): self._config['sortname'] = value
    sortname = property(__get_sortname, __set_sortname)

    def __get_viewrecords(self): return self._config['viewrecords']
    def __set_viewrecords(self, value): self._config['viewrecords'] = value
    viewrecords = property(__get_viewrecords, __set_viewrecords)
    
    def __get_sortorder(self): return self._config['sortorder']
    def __set_sortorder(self, value): self._config['sortorder'] = value
    sortorder = property(__get_sortorder, __set_sortorder)

    def __get_caption(self): return self._config['caption']
    def __set_caption(self, value): self._config['caption'] = value
    caption = property(__get_caption, __set_caption)
        
    def __get_toolbar(self): return self._config['toolbar']
    def __set_toolbar(self, value): self._config['toolbar'] = value
    toolbar = property(__get_toolbar, __set_toolbar)
    