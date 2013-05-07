#encoding=UTF-8
from atlcore.vcl.components import Component, Plugin
from atlcore.settings import JSLIBRARY, MEDIA_URL
#import simplejson as json
from django.utils import simplejson as json
import re

class JSTreeNode(object):
    # text: Texto que se muestra en el elementro del tree
    # url: Url para donde se envía cuando se da clic sobre el elemento 
    # children: Listado de hijos del elemento que también son TreeItems
    
    def __init__(self, id, text=None, url=None):
        self.id = id
        self.text = text
        self.url = url
        self.children = []
        self.parent = None

class JSTree(Component):
    
    
    def __init__(self, data_provider, version=None):
        super(JSTree, self).__init__(data_provider, version)
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._librarylist += [{'lib_jquery.jstree' : JSLIBRARY['lib_jquery.jstree']}]
        self.core = Plugin()
        self.core.html_titles = False
        self.core.animation = 500
        self.core.initially_open = []
        self.core.initially_load = []
        self.core.load_open = False
        self.core.open_parents = True
        self.core.notify_plugins = True
        self.core.rtl = False
        self.core.strings = { 'loading' : "Loading ...", 'new_node' : "New node" }
        self.themes = Plugin()
        self.themes.themes = "default"
        self.themes.url = "%scommon/js/jquery.plugins/jstree/themes/default/style.css" % MEDIA_URL
        self.plugins = ["themes", "json_data"]
   
    def html_tree(self, children = None):
        if not children:
            html_data = '<div id="%s">' % self.id
            datasource = self.nodes
        else:
            html_data = ''
            datasource = children
        html_data += '<ul>'
        for node in datasource:
            #TODO: Hacer que sea configurable la URL de los nodos
            html_data += '<li id="%s"> <a href="%s">%s</a>'%(node.id, node.url, node.text)
            if len(node.children) > 0:
                html_data += self.html_tree(node.children)
            html_data += '</li>'
        html_data += '</ul>'
        if not children:
            html_data += '</div>'
        return html_data
