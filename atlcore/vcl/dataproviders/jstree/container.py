#encoding=UTF-8

from django.conf.urls.defaults import patterns, url
from django.db.models import Q
from django.shortcuts import render_to_response
from atlcore.vcl.dataproviders.jstree import JSTreeDataProvider
from atlcore.contenttype.models import Container
#import simplejson as json
from django.utils import simplejson as json
from django.utils.translation import get_language
from atlcore.settings import ADMIN_PREFIX

class JSTreeContainerProvider(JSTreeDataProvider):
    """ 
       Suministra en forma de arbol los contenedores de atlcore partiendo de un contenedor dado
    """
    def __init__(self, container=None):
        self.container = container
        self.url = '/%s/jstreecontainer/get_json_data/' % ADMIN_PREFIX
        
    @classmethod    
    def get_urls(self):
        
        my_urls = patterns('',
            #url(r'^jstreecontainer/get_json_data/$', JSTreeContainerProvider.get_data, name='jstreecontainergetdata'),
            url(r'^jstreecontainer/get_json_data/$', JSTreeContainerProvider.get_data, name='jstreecontainergetdatafromid'),
            #url(r'^jstreecontainer/sortorder/$', self.sortorder, name="jstreecontainersortorder"),

        )
        return my_urls 

    @classmethod
    def __get_html_data(self, container_list):
        data = ''
        for i in container_list:
            data += '<li class="jstree-closed" id="%s"><a  href="%s">%s</a></li>' % (i.id, '#', i.title)
        return data

    @classmethod
    def __get_json_data(self, container_list):
        language = get_language()
        data = []
        for i in container_list:
            node = {}
            node['data'] = {'title': i.title, 'attr': { 'href': i.admin_url()}}
            node['attr'] = {'id': i.id, 'description': str(i.description), 'admin_url': i.admin_url()}
            child_list = Container.objects.filter(parent = i.id).order_by('-order')
            if len(child_list) > 0:
                node['state'] = 'closed'
            data.append(node)
        return data

    
    @classmethod
    def get_data(self,  request):
        language = get_language()
        if not (request.GET['id'] == '0'):
            container_list = Container.objects.filter(parent=request.GET['id']).filter(Q(language=language) | Q(neutral=True)).order_by('-order')
        else:
            container_list = Container.objects.filter(parent=None).filter(Q(language=language) | Q(neutral=True)).order_by('-order')
        data = self.__get_json_data(container_list)
        json_data = {}
        context = {
                   #'json_data' : json.dumps(json_data),
                   'data' : json.dumps(data)
        }
        return render_to_response('vcl/dataproviders/jstree/container/getdata.html', context)
    
    def json_open_tree(self, container=None):
        language = get_language()
        if container is None:
            container = self.container
        child_list = Container.objects.filter(parent=container).filter(Q(language=language) | Q(neutral=True)).order_by('-order')
        open_tree = JSTreeContainerProvider.__get_json_data(child_list)
        while container is not None:
            brothers = Container.objects.filter(parent=container.parent).filter(Q(language=language) | Q(neutral=True)).order_by('-order')
            json_brother_list = []
            for i in brothers:
                node = {}
                node['data'] = {'title': i.title, 'attr': { 'href': i.admin_url()}}
                node['attr'] = {'id': i.id, 'description': str(i.description), 'admin_url': i.admin_url()}
                child_list = Container.objects.filter(parent = i.id).filter(Q(language=language) | Q(neutral=True))
                if (len(child_list) > 0):
                    if i.id == container.id:
                        node['state'] = 'open'
                        node['children'] = open_tree
                    else:
                        node['state'] = 'closed'
                json_brother_list.append(node)
            if container.parent is None:
                container = None
            else:
                container = Container.objects.get(id=container.parent.id)
            open_tree = json_brother_list
        return json.dumps(open_tree) 
       