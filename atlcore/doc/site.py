#coding=UTF-8
from atlcore.site.base_site import BaseSite
from atlcore import settings as atlcore_settings
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from atlcore.vcl.components import JSTree, JSTreeNode, JQueryPlugin, JQGrid, JWPlayer, Button
import inspect

class DocSite(BaseSite):
    
    def __init__(self, name, app_name='doc'):
        super(DocSite, self).__init__(name=name, app_name=app_name)
        self.title = 'Documentación de AtlCore'
        description = 'Documentación de AtlCore.'
        keywords    = 'atlcore, atlantesoftware, documentación'
        
    def get_nav_menu(self):
        menu = [JSTreeNode('nav_componentes', 'Componentes', '#')]
        menu[0].children = [JSTreeNode('nav_jstree', 'JSTree', '/doc/jstree')]
        menu[0].children.append(JSTreeNode('nav_jqgrid', 'JQGrid', '/doc/jqgrid'))
        menu[0].children.append(JSTreeNode('nav_jqueryplugin', 'JQueryPlugin', '/doc/jqueryplugin'))
        menu[0].children.append(JSTreeNode('nav_jwplayer', 'JWPlayer', '/doc/jwplayer'))
        menu[0].children.append(JSTreeNode('nav_button', 'Button', '/doc/button'))
        nav_menu = JSTree(menu)
        nav_menu.id = 'nav_menu'
        return nav_menu
        
    def get_urls(self):
        urls = super(DocSite, self).get_urls()
        my_urls = patterns('',
            url(r'^doc/$', self.index, name='index'),
            url(r'^doc/jstree/$', self.jstree, name='jstree'),
            url(r'^doc/jqueryplugin/$', self.jqueryplugin_view, name='jqueryplugin'),
            url(r'^doc/jqgrid/$', self.jqgrid_view, name='jqgrid'),
            url(r'^doc/jqgrid/(?P<container_id>\d+)/$', self.jqgrid_view, name='jqgrid'),
            url(r'^doc/jwplayer/$', self.jwplayer_view, name='jwplayer'),
            url(r'^doc/jwplayer/(?P<video_id>\d+)/$', self.jwplayer_view, name='jwplayer'),
            url(r'^doc/button/$', self.button_view, name='button'),
        )
        return my_urls + urls
    
    def button_view(self, request):
        button = Button()
        button.label = 'prueba'
        button.theme = 'start'
        nav_menu = self.get_nav_menu()
        nav_menu.initially_open = ['nav_componentes', 'nav_jqgrid']
        context = {
               'nav_menu': nav_menu,
               'component': button,
               }
        return render_to_response('doc/show_component.html', context, context_instance=RequestContext(request))
    
    def jwplayer_view(self, request, video_id=None):
        jwplayer = JWPlayer()
        jwplayer.file = '%svideos/test.flv' % atlcore_settings.MEDIA_URL
        jwplayer.skin = '/media/bekle.zip'
        nav_menu = self.get_nav_menu()
        nav_menu.initially_open = ['nav_componentes', 'nav_jqgrid']
        context = {
               'nav_menu': nav_menu,
               'component': jwplayer,
               }
        return render_to_response('doc/show_component.html', context, context_instance=RequestContext(request))
      
    def index(self, request):
        context = {
               'nav_menu': self.get_nav_menu(),
               'mylinks': 'xxx',
               }
        return render_to_response('doc/index.html', context, context_instance=RequestContext(request))
    
    def jqgrid_view(self, request, container_id=None):
        from atlcore.vcl.datamodules import JQGridNode
        jqgrid = JQGrid(JQGridNode(container_id))
        jqgrid.id = 'mygrid'
        jqgrid.toolbar = ['true', 'top']
        button = Button()
        button.id = 't_mygrid'
        button.click = 'alert("ok");'
        button.label = 'New'
        jqgrid.toolbar_button_list = [button]
        nav_menu = self.get_nav_menu()
        nav_menu.initially_open = ['nav_componentes', 'nav_jqgrid']
        context = {
                   'nav_menu': nav_menu,
                   'component': jqgrid,
        }
        return render_to_response('doc/show_component.html', context, context_instance=RequestContext(request))

        
    
    def jqueryplugin_view(self, request):
        from atlcore.vcl.components import JQueryPlugin
        jqueryplugin = JQueryPlugin('Highcharts.Chart')
        jqueryplugin.id = 'chart1'
        jqueryplugin.librarylist += [{'lib_jquery': atlcore_settings.JSLIBRARY['lib_jquery']}]
        jqueryplugin.librarylist += [{'lib_highcharts.chart': atlcore_settings.JSLIBRARY['lib_highcharts.chart']}]
        jqueryplugin.config = { 'chart': {
                                    'renderTo': 'chart1',
                                    'defaultSeriesType': 'bar'
                                 },
                                 'title': {
                                    'text': 'Fruit Consumption'
                                 },
                                 'xAxis': {
                                    'categories': ['Apples', 'Bananas', 'Oranges']
                                 },
                                 'yAxis': {
                                    'title': {
                                       'text': 'Fruit eaten'
                                    }
                                 },
                                 'series': [{
                                    'name': 'Jane',
                                    'data': [1, 0, 4]
                                 }, {
                                    'name': 'John',
                                    'data': [5, 7, 3]
                                 }]
                              }
        nav_menu = self.get_nav_menu()
        nav_menu.initially_open = ['nav_componentes', 'nav_jqueryplugin']
        context = {
                   'nav_menu': nav_menu,
                   'jqueryplugin': jqueryplugin,
                   'documentation': inspect.getdoc(jqueryplugin.test),
                   }
        return render_to_response('doc/jqueryplugin.html', context, context_instance=RequestContext(request))
    
    def jstree(self, request):
        tree = [JSTreeNode('1', 'google', 'http://google.com'), 
                JSTreeNode('2', 'yahoo', 'http://yahoo.com')]
        tree[0].children = [JSTreeNode('3', 'videos', 'http://youtube.com')]
        jstree = JSTree(tree)
        jstree.id = 'demo_tree'
        nav_menu = self.get_nav_menu()
        nav_menu.initially_open = ['nav_componentes', 'nav_jstree']
        context = {
                   'nav_menu': nav_menu,
                   'jstree': jstree,
        }
        return render_to_response('doc/jstree.html', context, context_instance=RequestContext(request))    


